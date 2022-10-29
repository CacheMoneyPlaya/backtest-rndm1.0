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

    def next(self):
        # Simply log the closing price of the series from the reference
        try:
            self.data_history_index += 1
        except Exception as e:
            pass

        if self.data_history_index > 601:
            self.fvg_data_points = self.fvg.cycle_chunk(self.dataclose)
            print(self.fvg_data_points)
            cu.chart_fvg(self.fvg_data_points, self.dataclose.datetime[0])


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(FvgContainAndReject)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'Datasets/GOOG.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2006, 1, 1),
        # Do not pass values before this date
        todate=datetime.datetime(2022, 12, 31),
        # Do not pass values after this date
        reverse=False)

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
