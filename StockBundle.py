import pandas as pd
from StockLib.Stock import Stock
from StockLib.Stock import DATATYPE
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime as dt
import numpy as np

class Bundle:

    def __init__(self, tickers: list[str]):
        """
        Constructor for stocks bundle class

        :param tickers: list of strings storing the tickers of the stocks stored in the bundle
        """

        self.l_tickers: list[str] = tickers
        self.stocks: dict = {}

        self.close = pd.DataFrame()
        self.open = pd.DataFrame()
        self.high = pd.DataFrame()
        self.low = pd.DataFrame()
        self.volume = pd.DataFrame()

        for ticker in tickers:
            self.stocks[ticker] = Stock(ticker,load_local={'bool':True})
        self.__setattrvalues__()

    def __getitem__(self, key:list[str]):
        d = {}
        for k in key:
            if self.stocks.get(k) != None:
                d[k] = self.stocks.get(k)
            else:
                raise KeyError(k)
        return d


    def download(self, 
                 start: dt.datetime = None,
                 end: dt.datetime = None,
                 period: str = '',
                 interval: str = '1d',
                 datatype: str = 'all',
                 overwrite: str = False,
                 ):
        """
        Method dowloading stocks info via `YahooFinance <https://finance.yahoo.com/>`_

        :param start: datetime.datetime object for the beginning of the data acquisition
        :param end: datetime.datetime object for the end of the data aquisition. 
        :param period: String describing the period to acquire. Valid entries 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        :param interval: String describing the data frequency. Valid entries 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        :param datatype: String describing the type needed. 'all' for all the data
        :return: Dictionnary compiling yfinance data"
        """

        for stock in self.stocks.values():
            stock.download(start,end,period,interval,overwrite=overwrite)
            self.__setattrvalues__()

    def __setattrvalues__(self):
        for stock in self.stocks.values():
            self.close[stock.ticker] = stock.close
            self.open[stock.ticker] = stock.open
            self.high[stock.ticker] = stock.high
            self.low[stock.ticker] = stock.low
            self.volume[stock.ticker] = stock.volume

    def plotcandles(self):
        """
        Displays candles for the stocks in the :Stock: object
        """

        nstocks = len(self.l_tickers)
        rows = int(np.ceil(np.sqrt(nstocks)))
        cols = int(np.ceil(nstocks / rows))

        lay = go.Layout(
            template='plotly_dark',
            legend={'visible':False}
        )

        fig = make_subplots(
            rows=rows, 
            cols=cols,
            subplot_titles=self.l_tickers
            )
        fig.update_layout(
            lay,
            title={
                'text':'BUNDLE DISPLAY',
                'y':0.96,
                'x':0.5,
                'xanchor':'center',
                'yanchor':'top',
                'font': {'size':40,'family':'Arial, sans-serif'}
                }            
        )

        i,j = (1,1)
        iter = 1
        
        for stock in self.stocks.values():

            candle_trace = stock.plotcandle('svg')

            fig.add_trace(
                candle_trace,
                row=i,
                col=j
            )
            fig.update_layout(
                {f'xaxis{iter}': {"autorange": True, "rangeslider": {'visible': False}}}
            )
            if j==cols:
                i+=1
                j=1
            else:
                j+=1
            iter+=1
            
        fig.show()
