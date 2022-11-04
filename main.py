from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd

from Indicators.Fvg import Fvg

import backtrader as bt

from Charting import chart_utils as cu

class FvgContainAndReject(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0]
        self.data_history_index = 0
        self.fvg = Fvg()
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
                        'ATOM BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))
                else:  # Sell
                    self.log('ATOM SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                             (order.executed.price,
                              order.executed.value,
                              order.executed.comm))
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

    def next(self):
        self.count +=1
        if self.stats.broker.value[0] < 10:
            self.log('BACKTEST EXHAUSTION!')
            exit()

        try:
            self.data_history_index += 1
        except Exception as e:
            pass

        if self.data_history_index > 500:

            self.positioned = False

            adjusted_size = 0.3*self.broker.getcash()/self.dataclose.close[0]

            self.fvg_data_points = self.fvg.cycle_chunk(self.dataclose)
            long_entry = self.fvg.long()
            short_entry = self.fvg.short()

            if not self.position and not self.positioned and long_entry['acceptance']:
                take_profit_price = 1.05 * self.dataclose.close[0]
                stop_price = (long_entry['fvg']['fvg_low'] + long_entry['fvg']['fvg_high'])
                self.buy_bracket(size=adjusted_size, limitprice=take_profit_price, stopprice=stop_price, exectype=bt.Order.Market)
                self.positioned = True

            if not self.position and not self.positioned and short_entry['acceptance']:
                take_profit_price = 0.95 * self.dataclose.close[0]
                stop_price = (short_entry['fvg']['fvg_high'] + short_entry['fvg']['fvg_low'])
                self.sell_bracket(size=adjusted_size, limitprice=take_profit_price, stopprice=stop_price, exectype=bt.Order.Market)
                self.positioned = True

            # if self.count == 3445:
            #     cu.chart_fvg(self.fvg_data_points, self.dataclose.datetime.datetime(0))
            #     exit()


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(FvgContainAndReject)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'Datasets/Data/algo_binance_datetime.csv')

    data = bt.feeds.GenericCSVData(
            dataname=datapath,
            fromdate=datetime.datetime(2020, 8, 17),
            todate=datetime.datetime(2022, 11, 3),
            nullvalue=0.0,
            dtformat='%Y-%m-%d %H:%M:%S',
            timeframe=bt.TimeFrame.Minutes,
            datetime=0,
            open = 1,
            high = 2,
            low = 3,
            close = 4,
            volume =5,
            openinterest=-1,
            plot=False
        )

    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.broker.set_shortcash(False)
    cerebro.broker.setcommission(commission=0.0015, margin = None, mult = 10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
