import pandas as pd
import plotly.graph_objects as go


class _Indicator():
    """
    Private Class storing indicator data
    """

    def __init__(self, stock):
        '''
        Constructor

        :param stock: *Stock* object to apply the indicator

        '''
        
        self.stock = stock
        self.data:dict = {
            'onstock': {},
            'indicator': {}
        }

        try:
            test = stock.ticker
        except:
            raise AssertionError(f'Stock {stock} does not exist')
        
    def __setdata__(self, data: pd.DataFrame, style):
        return {
            'data':data,
            'style':style
        }
    
    def get_rawdata(self):

        df = pd.DataFrame(index=self.stock._yfdata.index)

        indic:dict = self.data['indicator']
        onstock: dict = self.data['onstock']

        for indicator_key, indicator_dict in indic.items():
            df[indicator_key] = indicator_dict['data'].values

        for onstock_key, onstock_dict in onstock.items():
            df[onstock_key] = onstock_dict['data'].values
    
        return df


        


class MACD(_Indicator):

    def __init__(self, stock, serie: pd.DataFrame = pd.DataFrame(), a:float = 12,b:float = 26,c:float = 9):
        '''
        Mean Averaged Convergence Divergence (Indicator)

        :param stock: *Stock* object to apply the indicator
        :param serie: Dataframe to apply MACD to, CLOSE data if ommited
        :param a: EMA Slow
        :param b: EMA Fast
        :param c: Signal
        :returns: Dataframe
        '''

        super().__init__(stock)

        input_serie = serie
        if serie.empty:
            input_serie:pd.DataFrame = stock._yfdata['Close']

        fast_ema = input_serie.ewm(span=a, min_periods=a).mean()
        slow_ema = input_serie.ewm(span=b, min_periods=b).mean()
        macd = fast_ema - slow_ema
        signal = macd.ewm(span=c, min_periods=c).mean()
        self.data['indicator']['MACD'] = self.__setdata__(macd,go.Scatter)
        self.data['indicator']['sig'] = self.__setdata__(signal,go.Scatter)
        self.data['indicator']['deltaMACD'] = self.__setdata__(signal-macd,go.Bar)

    
