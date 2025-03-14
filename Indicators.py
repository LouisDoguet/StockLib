import pandas as pd
import plotly.graph_objects as go


class _Indicator():
    """
    Private Class storing indicator data
    """

    def __init__(self, stock, serie:pd.DataFrame = pd.DataFrame()):
        '''
        Constructor

        :param stock: *Stock* object to apply the indicator

        '''
        
        self.stock = stock
        self.data:dict = {
            'onstock': {},
            'indicator': {}
        }

        self.input = serie

        try:
            stock._yfdata
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

    def __init__(self, stock, serie:pd.DataFrame = pd.DataFrame(),a:float = 12,b:float = 26,c:float = 9):
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

        if serie.empty:
            input:pd.DataFrame = self.stock._yfdata['Close']

        fast_ema = input.ewm(span=a, min_periods=a).mean()
        slow_ema = input.ewm(span=b, min_periods=b).mean()
        macd = fast_ema - slow_ema
        signal = macd.ewm(span=c, min_periods=c).mean()
        self.data['indicator']['MACD'] = self.__setdata__(macd,go.Scatter)
        self.data['indicator']['sig'] = self.__setdata__(signal,go.Scatter)
        self.data['indicator']['deltaMACD'] = self.__setdata__(signal-macd,go.Bar)

    
class ATR(_Indicator):

    def __init__(self, stock, n:int = 14):
        '''
        Average True Rate
        :param stock: *Stock* object to apply the indicator
        :param n: Period
        :returns: Dataframe
        '''

        super().__init__(stock)

        self.input = pd.DataFrame(columns=['c_high','c_low','p_close'])
        self.input['c_high'] = self.stock._yfdata['High']
        self.input['c_low'] = self.stock._yfdata['Low']
        self.input['p_close'] = self.stock._yfdata['Close'].shift(1)
        
        df = pd.DataFrame()
        df["HL"] = self.input['c_high'] - self.input['c_low']
        df["HPC"] = abs(self.input['c_high'] - self.input['p_close'])
        df["HPL"] = abs(self.input['c_low'] - self.input['p_close'])

        TR = df.max(axis=1,skipna=False)
        ATR = TR.ewm(alpha=1/n, min_periods=n).mean()

        self.data['onstock']['TR'] = self.__setdata__(TR, go.Scatter)
        self.data['onstock']['ATR'] = self.__setdata__(ATR, go.Scatter)


class BollingerBands(_Indicator):

    def __init__(self, stock, n:int = 20, k:float = 2):
        '''
        Bollinger Bands

        :param stock: *Stock* object to apply the indicator
        :param n: Period
        :param k: Multiplier
        :returns: Dataframe
        '''

        super().__init__(stock)

        self.input:pd.DataFrame = self.stock._yfdata['Close']

        rolling_mean = self.input.rolling(window=n).mean()
        rolling_std = self.input.rolling(window=n).std()

        upper_band = rolling_mean + (rolling_std * k)
        lower_band = rolling_mean - (rolling_std * k)

        self.data['onstock']['Upper band'] = self.__setdata__(upper_band, go.Scatter)
        self.data['onstock']['Lower band'] = self.__setdata__(lower_band, go.Scatter)
        self.data['onstock']['Rolling mean'] = self.__setdata__(rolling_mean, go.Scatter)
        self.data['indicator']['Delta'] = self.__setdata__(upper_band-lower_band, go.Bar)


class RSI(_Indicator):
    
    def __init__(self, stock, n:int = 14):
        '''
        Relative Strength Index

        :param stock: *Stock* object to apply the indicator
        :param n: Period
        :returns: Dataframe
        '''

        super().__init__(stock)

        self.input:pd.DataFrame = self.stock._yfdata['Close']

        delta = self.input.diff()
        avg_gain = (delta.where(delta > 0, 0)).ewm(alpha=1/n, min_periods=n).mean()
        avg_loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/n, min_periods=n).mean()

        RS = avg_gain / avg_loss
        RSI = 100 - (100 / (1 + RS))

        self.data['indicator']['RSI'] = self.__setdata__(RSI, go.Scatter)


class ADX(_Indicator):

    def __init__(self, stock, n:int = 14):
        '''
        Average Directional Index

        :param stock: *Stock* object to apply the indicator
        :param n: Period
        :returns: Dataframe
        '''

        super().__init__(stock)

        self.input:pd.DataFrame = self.stock._yfdata
        H = self.input['High']
        L = self.input['Low']

        df = pd.DataFrame()
        df['ATR'] = ATR(stock,n).get_rawdata()['ATR']
        df['PDM'] = H - H.shift(1)
        df['NDM'] = L.shift(1) - L
        df['PDM'] = df['PDM'].where((df['PDM'] > 0) & (df['PDM'] > df['NDM']), 0)
        df['NDM'] = df['NDM'].where((df['NDM'] > 0) & (df['NDM'] > df['PDM']), 0)
        df['PDI'] = (df['PDM'].ewm(com=n, min_periods=n).mean() / df['ATR']) * 100
        df['NDI'] = (df['NDM'].ewm(com=n, min_periods=n).mean() / df['ATR']) * 100
        DX = abs(df['PDI'] - df['NDI']) / (df['PDI'] + df['NDI']) * 100
        ADX = DX.ewm(alpha=1/n, min_periods=n).mean()

        #self.data['indicator']['DX'] = self.__setdata__(DX, go.Scatter)
        self.data['indicator']['ADX'] = self.__setdata__(ADX, go.Scatter)
