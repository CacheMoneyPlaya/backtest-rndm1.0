# Charting
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
import matplotlib.patches as mpatches
import datetime as dt
from matplotlib.patches import Rectangle

def chart_fvg(fvg_data_points, x_current):
    plt.style.use('ggplot')
    context = mpl_dates.date2num(x_current)

    # Extracting Data for plotting
    data = pd.read_csv('Datasets/Data/ATOM_binance_datetime.csv').head(3500)
    ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    ohlc['Date'] = pd.to_datetime(ohlc['Date'])
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)
    ohlc = ohlc.astype(float)

    # Creating Subplots
    fig, ax = plt.subplots()

    candlestick_ohlc(ax, ohlc.values, width=0.01, colorup='green', colordown='red', alpha=0.8)

    # Setting labels & titles
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    fig.suptitle('btc-binance')

    # Formatting Date
    date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    for dp in fvg_data_points['delta_p']:
        if not dp['fvg_invalidated']:
            start = mpl_dates.date2num(dp['fvg_timestamp'])
            date_delta = context-start
            fvg_delta = dp['fvg_high'] - dp['fvg_low']
            ax.add_patch(Rectangle((start, dp['fvg_low']), date_delta, fvg_delta, color='green', alpha=0.5))

    for dp in fvg_data_points['delta_n']:
        if not dp['fvg_invalidated']:
            start = mpl_dates.date2num(dp['fvg_timestamp'])
            date_delta = context - start
            fvg_delta = dp['fvg_high'] - dp['fvg_low']
            ax.add_patch(Rectangle((start, dp['fvg_low']), date_delta, fvg_delta, color='red', alpha=0.5))

    plt.show()
