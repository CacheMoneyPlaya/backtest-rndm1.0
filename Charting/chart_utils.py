# Charting
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
import matplotlib.patches as mpatches
import datetime as dt

def chart_fvg(fvg_data_points, x_current):
    plt.style.use('ggplot')

    # Extracting Data for plotting
    data = pd.read_csv('Datasets/GOOG.csv')
    ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    ohlc['Date'] = pd.to_datetime(ohlc['Date'])
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)

    # Creating Subplots
    fig, ax = plt.subplots()

    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

    # Setting labels & titles
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    fig.suptitle('GOOG')

    # Formatting Date
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    ax.axvline(dt.datetime(2008, 6, 7))

    for dp in fvg_data_points['delta_p']:
        plt.axhspan(dp['fvg_low'], dp['fvg_high'], color='green', alpha=0.5, lw=0)

    for dp in fvg_data_points['delta_n']:
        plt.axhspan(dp['fvg_low'], dp['fvg_high'], color='red', alpha=0.5, lw=0)

    plt.show()
