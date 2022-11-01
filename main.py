from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd

from Indicators.Fvg import Fvg

# Import the backtrader platform
import backtrader as bt

# Charting
from Charting import chart_utils as cu

# Create a Stratey
class FvgContainAndReject(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the open, close, high, low as a comprehension
        self.dataclose = self.datas[0]
        self.data_history_index = 0
        self.fvg = Fvg()
        self.count = 0

    def next(self):
        # Simply log the closing price of the series from the reference
        try:
            self.data_history_index += 1
        except Exception as e:
            pass

        if self.data_history_index > 2001:
            self.fvg_data_points = self.fvg.cycle_chunk(self.dataclose)
            self.count +=1
            cu.chart_fvg(self.fvg_data_points, self.dataclose.datetime.datetime(0))
            exit()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(FvgContainAndReject)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'Datasets/Data/btc_binance_datetime.csv')

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2020, 8, 17),
        todate=datetime.datetime(2022, 11, 1),
        nullvalue=0.0,
        dtformat='%Y-%m-%d %H:%M:%S',
        timeframe=bt.TimeFrame.Minutes,
        datetime=0,
        open = 1,
        high = 2,
        low = 3,
        close = 4,
        volume =5,
        openinterest=-1)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
