import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json

class StockPlot():

    def __init__(self,stock):
        path = os.getcwd() + '/StockLib/plotlydata.json'
        f = open(path)
        content = f.read()
        plotlydata = json.loads(content)

        self.stock = stock
        self._plotlydata = plotlydata
        self.layout:dict = plotlydata['layout']
        self.__init_layout__()
        self.candlesticks:dict = plotlydata['stockdata']['candle_data']
        self.__init_candles__()
        f.close()

    def __init_layout__(self):
        self.layout['title']['text'] = self.stock.ticker
    
    def __init_candles__(self):
        dates=self.stock._yfdata.index
        stockdata = self.stock._yfdata
        self.candlesticks['x'] = dates
        self.candlesticks['open'] = stockdata['Open']
        self.candlesticks['high'] = stockdata['High']
        self.candlesticks['low'] = stockdata['Low']
        self.candlesticks['close'] = stockdata['Close']


    def plotcandle(self):
        
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=[self.stock.ticker,''],
            row_heights=[0.8,0.2]
        )

        fig.update_layout(go.Layout(self.layout))

        fig.add_trace(
            trace=go.Candlestick(self.candlesticks),
            row=1,
            col=1
        )

        return fig, go.Candlestick(self.candlesticks)