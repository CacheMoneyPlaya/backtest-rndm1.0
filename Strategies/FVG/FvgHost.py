from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import sys
import pandas as pd
from Strategies.FVG.FvgStrategy import FvgStrategy
import backtrader as bt
from Charting import chart_utils as cu

class FvgHost(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0]
        self.data_history_index = 0
        self.fvg = FvgStrategy()
        self.count = 0
        self.ev_trades_count = {
            'p_ev': 0,
            'n_ev': 0,
        }

    def notify_trade(self,trade):
        if not trade.isclosed:
            return

        if self.broker.orders:
            [self.cancel[o] for o in self.broker.orders if o.status < 4]

        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
            trade.pnl, trade.pnlcomm))

        if trade.pnl >= 0:
            self.ev_trades_count['p_ev'] +=1
        else:
            self.ev_trades_count['n_ev'] +=1

        self.log('Trade tally, +EV: {}, -EV: {}'.format(self.ev_trades_count['p_ev'], self.ev_trades_count['n_ev']))

    def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                return

            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log(
                        'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))
                else:  # Sell
                    self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                             (order.executed.price,
                              order.executed.value,
                              order.executed.comm))
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

    def next(self):
        self.count +=1
        try:
            self.data_history_index += 1
        except Exception as e:
            pass

        if self.data_history_index > 800:
# (long_entry['fvg']['fvg_low'] + long_entry['fvg']['fvg_high']) / 2
            adjusted_size = 0.3*self.broker.getcash()/self.dataclose.close[0]

            self.fvg_data_points = self.fvg.cycle_chunk(self.dataclose)
            long_entry = self.fvg.long()
            short_entry = self.fvg.short()

            if not self.position and long_entry['acceptance']:
                take_profit_price = 1.02 * self.dataclose.close[0]
                stop_price = long_entry['fvg']['fvg_low']
                self.buy_bracket(size=adjusted_size, limitprice=take_profit_price, stopprice=stop_price, exectype=bt.Order.Market)

            if not self.position and short_entry['acceptance']:
                take_profit_price = 0.98 * self.dataclose.close[0]
                stop_price = short_entry['fvg']['fvg_high']
                self.sell_bracket(size=adjusted_size, limitprice=take_profit_price, stopprice=stop_price, exectype=bt.Order.Market)

            # if self.count == 3445:
            #     cu.chart_fvg(self.fvg_data_points, self.dataclose.datetime.datetime(0))
            #     exit()
