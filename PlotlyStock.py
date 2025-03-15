import pandas as pd
import plotly.graph_objects as go
import StockLib.Indicators as ind
from plotly.subplots import make_subplots
import os
import json

path = os.getcwd() + '/StockLib/plotlydata.json'
f = open(path)
content = f.read()
plotlydata = json.loads(content)
INDICATORS = str(plotlydata['indicators'].keys())
f.close()

class StockPlot():
    ''''
    Class hadling PLOTLY objects
    '''

    def __init__(self,stock):
        '''
        Simple handling of Plotly lib for *StockLib* uses

        :param stock: *Stock* object to translate in Plotly objects to plot
        '''

        self.stock = stock
        self.dates = self.stock._yfdata.index
        self._plotlydata = plotlydata
        self.layout:dict = plotlydata['layout']
        self.__init_layout__()
        self.candlesticks:dict = plotlydata['stockdata']['candle_data']
        self.__init_candles__()

        self.line = plotlydata['indicators']['line']
        self.upperband = plotlydata['indicators']['upperband']
        self.lowerband = plotlydata['indicators']['lowerband']
        self.bar = plotlydata['indicators']['bar']

        self.indicators_objects:dict = {}

        for key,ind in stock.indicators.items():
            self.indicators_objects[key] = self.__getplotly__(ind)

    def __init_layout__(self):
        '''
        Layout initialization
        '''
        self.layout['title']['text'] = self.stock.ticker
    
    def __init_candles__(self):
        '''
        *go.Candlesticks object initialization*
        '''

        stockdata = self.stock._yfdata
        self.candlesticks['x'] = self.dates
        self.candlesticks['open'] = stockdata['Open']
        self.candlesticks['high'] = stockdata['High']
        self.candlesticks['low'] = stockdata['Low']
        self.candlesticks['close'] = stockdata['Close']

    def __get_line__(self,data:pd.DataFrame,color:str=None):
        '''
        *go.Scatter object initialization*
        '''
        dates=self.dates
        self.line['x'] = dates
        self.line['y'] = data
        self.line['line']['color'] = color
        self.line['name'] = data.Name

        return go.Scatter(self.line)

    def __get_upperband__(self,data):
        self.upperband['x'] = self.dates
        self.upperband['y'] = data
        self.upperband['name'] = data.Name

        return go.Scatter(self.upperband)

    def __get_lowerband__(self,data):
        self.lowerband['x'] = self.dates
        self.lowerband['y'] = data
        self.lowerband['name'] = data.Name

        return go.Scatter(self.lowerband)

    def __get_bar__(self, data):
        self.bar['x'] = self.dates
        self.bar['y'] = data
        self.bar['name'] = data.Name

        return go.Bar(self.bar)

    

    def __getplotly__(self, indicator: ind._Indicator):
        '''
        From an indicator, get the Plotly objects filled with indicator's data

        :param indicator: Indicator object
        :return: dict['onstock'= [go.Objects] , 'indicator'= [go.Objects]]
        '''

        onstock:dict = indicator.data['onstock']
        indic:dict = indicator.data['indicator']

        go = dict(onstock={}, indicator={})

        for key,dictval in onstock.items():
            plotstyle = dictval['style']
            dataset = dictval['data']
            color = dictval['color']
            go['onstock'][key] = self.setstyle(dataset,plotstyle,color)

        for key,dictval in indic.items():
            plotstyle = dictval['style']
            dataset = dictval['data']
            color = dictval['color']
            go['indicator'][key] = self.setstyle(dataset,plotstyle,color)

        return go


    def setstyle(self, dataset, style, color=None):

        match style:

            case 'line':
                stl = self.__get_line__(dataset,color)
            
            case 'upperband':
                stl = self.__get_upperband__(dataset)

            case 'lowerband':
                stl = self.__get_lowerband__(dataset)
            
            case 'bar':
                stl = self.__get_bar__(dataset)
            
            case _:
                raise ValueError(f'Type of PlotlyStock object not recognised ({type(style)})')
            
        return stl


    def plotcandle(self):
        '''
        Creates the candle plot of the stock
        '''
        
        fig = go.Figure()
        fig.update_layout(go.Layout(self.layout))
        fig.add_trace(trace=go.Candlestick(self.candlesticks))

        return fig, go.Candlestick(self.candlesticks)
    
    def plot(self):
        '''
        Plots the Candle chart and the loaded indicators
        '''

        fig = go.Figure()

        fig = make_subplots(
            rows=2,
            cols=1,
            row_heights=[0.7,0.3],
            shared_xaxes=True,
            vertical_spacing=0.02
        )

        fig.add_trace(
            go.Candlestick(self.candlesticks),
            row=1,
            col=1
        )

        for indic,ind_keys in self.indicators_objects.items():
            for keys,g in ind_keys['onstock'].items():
                fig.add_trace(
                    g,
                    row=1,
                    col=1
                )
            for keys,g in ind_keys['indicator'].items():
                fig.add_trace(
                    g,
                    row=2,
                    col=1
                )

        fig.update_layout(go.Layout(self.layout))

        fig.show()

    
    def plotindicator(self):
        '''
        Plot an indicator on the stock plot

        :param indicator: *Indicator* object to plot
        '''

        for ind_key, ind_obj in self.indicators_objects.items():
            cdlfig = go.Figure()
            indfig = go.Figure()
            if len(ind_obj['onstock']) != 0:
                for keys,g in ind_obj['onstock'].items():
                    cdlfig.add_trace(g)
            if len(ind_obj['indicator']) != 0:
                for keys,g in ind_obj['indicator'].items():
                    indfig.add_trace(g)