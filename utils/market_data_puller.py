import yfinance as yf
import pandas as pd


def get_stock_data(stock, period='1df', interval='1m'):
    return yf.download(
        tickers=stock.upper(),
        period=period,
        interval=interval
    )


def calc_market_stats(data, stock):
    _open = data.iloc[0].Open
    _high = data.High.max()
    _low = data.Low.min()
    _close = data.iloc[-1].Close
    _change = _close - _open
    _perc_change = _change / _open * 100
    _volume_k = sum(data.Volume) / 1000
    _turnover_m = _volume_k * ((_open + _close) / 2) / 1000
    _row = [_open, _high, _low, _close, _change, _perc_change, _volume_k, _turnover_m]
    return pd.DataFrame(
        [_row],
        columns=['Open', 'High', 'Low', 'Close', 'Change', '%_Change', 'Total Volume (K)', 'Turnover (M)'],
        index=[stock]
    )
