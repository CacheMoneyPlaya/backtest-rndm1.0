from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd

from Indicators.Fvg import Fvg

# Import the backtrader platform
import backtrader as bt


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
            # print('Date {}, Open {} , Close, {} , Low, {}, High, {}'.format(self.dataclose.datetime[0], self.dataclose.open[0], self.dataclose.close[0], self.dataclose.low[0], self.dataclose.high[0]))
        except Exception as e:
            pass

        if self.data_history_index > 301:
            # print('previous values were')
            # print('Date {}, Open {} , Close, {} , Low, {}, High, {}'.format(self.dataclose.datetime[-1], self.dataclose.open[-1], self.dataclose.close[-1], self.dataclose.low[-1], self.dataclose.high[-1]))
            self.fvg.cycle_chunk(self.dataclose)

        # Need to be able to provide a chunk of data to some arbitrary method i.e. all of dataclose data from 0 -> -300
        # Method then takes data in steps of 3 i.e. -300,-299,-298
        # We make two checks using:
        # Positive delta checking close1 < close2 < close3
        # Negative delta checking close1 > close2 > close3
        #
        # See if we have any fvg's between these, will need to find a way to see if they have been historically invalidated
        # So after finding these fvg's look at all closes from point of fvg onwards for any positions where said close has moved higher or lower
        # This could be quite intensive to run but on something like 15 min could be ok
        #
        # Once we have the FVG's identified we will need to check to see if current candle closes outside + previous closes in which is all thats needed, yeah we can
        # get more technical with it having x number of candles not closing in etc




        # Create a grouping of FVG's that have previously existed in last 600 days and check no closes
        # have happened above them i.e. still active in both directions, this being run on any
        # new candle close will mean we will be able to remove invalidated before calling

        # Run a check to see if we have had any candles close below or above it
        # that do not include the candle that formed it so point of creation + 1

        # Then check we have had any entries into the fvg which have closed inside

        # Then check we have any that have closed outside in the direction of the bias

        # Make decision based on this


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
