import yfinance as yf
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from StockLib.utils import scrap_url, create_arbo
from StockLib.PlotlyStock import StockPlot
import StockLib.Indicators as ind
import types
import os

DATATYPE = ['Open','High','Low','Close','Volume']

class Stock:
    """
    *Stock* class storing stock infos and methods
    """

    def __init__(self, ticker: str, load_local:dict = None):
        """
        Class constructor creating a *Stock* instance

        :param ticker: 
        Ticker string (yfinance)
        """

        self.ticker:str = ticker
        self._arbo:dict = {}

        if load_local is None:  # Initialisation propre du dictionnaire
            load_local = {}
            load_local['bool'] = True
            self._arbo['path'] = os.getcwd() + '/StockData'

        try:
            self._arbo['path'] = load_local['path']
        except:
            self._arbo['path'] = os.getcwd() + '/StockData'


        jsonpath, svgpath = create_arbo(self._arbo['path'],self.ticker)[1:]
        self._arbo['bool'] = True

        self._arbo['json'] = {
            'path':jsonpath,
            'filepath':jsonpath+'/{}.json'.format(str.replace(ticker,'.','-'))
            }
        self._arbo['svg'] = {
            'path':svgpath,
            'filepath':svgpath+'/{}.svg'.format(str.replace(ticker,'.','-'))
            }

        self._yfdata: pd.DataFrame = pd.DataFrame()
        self._svg: go.Figure = go.Figure()

        try:
            self._yfdata = pd.read_json(self._arbo['json']['filepath'])
            self._yfdata.columns = DATATYPE
            self.__setvalues__()
            self.__stockprint__(f'Data loaded. ({self._arbo['path']})')
        except:
            self.__stockprint__('Empty stock object created, no data loaded.')

    def __setvalues__(self):

        for dtype in DATATYPE:
            setattr(self, dtype.lower(), self._yfdata[dtype])
        self.__setmet__(self.pct)
        self.__setmet__(self.MACD)

    def __setmet__(self,method:types.MethodType):

        for attrname in list(self.__dict__.keys()):
            if attrname in [dt.lower() for dt in DATATYPE]:
                setattr(
                    self.__getattribute__(attrname), 
                    method.__name__,
                    lambda serie=self.__getattribute__(attrname): method(serie=serie)
                    )
            
    def MACD(self,serie=pd.DataFrame(),a:float = 12,b:float = 26,c:float = 9):
        '''
        Mean Averaged Convergence Divergence (Indicator)

        :param a: EMA Slow
        :param b: EMA Fast
        :param c: Signal
        :returns: Dataframe
        '''
        return ind.MACD(self,serie,a,b,c).get_rawdata()


    def pct(self,serie:pd.DataFrame = pd.DataFrame()):
        '''
        Percentage Change of the stock
        '''
        if serie.empty:
            serie = self._yfdata
        return serie.pct_change()

    def download(self, 
                 start: dt.datetime = None,
                 end: dt.datetime = None,
                 period: str = '',
                 interval: str = '1d',
                 datatype: str = 'all',
                 overwrite: bool = False):
        """
        Method dowloading stock info via `YahooFinance <https://finance.yahoo.com/>`_

        :param start: datetime.datetime object for the beginning of the data acquisition
        :param end: datetime.datetime object for the end of the data aquisition. 
        :param period: String describing the period to acquire. Valid entries 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        :param interval: String describing the data frequency. Valid entries 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        :param datatype: String describing the type needed. 'all' for all the data
        :return: Dictionnary compiling yfinance data
        """

        if not self._yfdata.empty:
            if overwrite == True:
                self._yfdata = pd.DataFrame()
                self.__stockprint__("OVERWRITE - Data deleted.")
                return self.download(start,end,period,interval,datatype,overwrite=False)
            else:
                pass
                return self._yfdata

        bool_period = (end == None and start == None and period != '')
        bool_start_end = (start != None and period == '')

        stock_data = pd.DataFrame()

        if (bool_period == False) and (bool_start_end == False):
            raise ValueError('No period nor start/end couple entered')
        
        elif (bool_period == True) and (bool_start_end == True):
            raise ValueError('Period and stard end entered')
        
        else:

            if end == None:
                end = dt.datetime.today()

            try:
                match bool_period:
                    case True:
                            stock_data = yf.download(
                                tickers=[self.ticker],
                                period=period,
                                interval=interval,
                                multi_level_index=False,
                                auto_adjust=True
                                )
                    
                    case False:
                            stock_data = yf.download(
                                tickers=[self.ticker],
                                start=start,
                                end=end,
                                interval=interval,
                                multi_level_index=False,
                                auto_adjust=True
                                )
                self.__stockprint__('DOWNLOAD - Stock downloaded sucessfully')
            except:
                raise self.__stockprint__('DOWLOAD ERROR')

        self._yfdata:pd.DataFrame = stock_data
        self._yfdata.columns = DATATYPE
        self.__setvalues__()

        self.save_data()
        if datatype in DATATYPE:
            return stock_data[datatype]
        else:
            return stock_data
        

        
    def plotcandle(self,renderer:str = ''):
        """
        Candle plot of the *Stock* object
        """

        try:
            df = self._yfdata
            dates=self._yfdata.index
        except:
            raise ValueError('Stock not downloaded. Use .download() method')
        
        fig, cdata = StockPlot(self).plotcandle()
        
        self._svg = fig
        if renderer == '':
            fig.show()
        elif renderer == 'svg':
            self.__stockprint__('PLOTCANDLE - SVG file created and saved')

        self.save_data()
        return cdata

    def scrap_financials(self):
        cfURL = 'https://finance.yahoo.com/quote/{tick}/cash-flow/'.format(tick=self.ticker)
        bsURL = 'https://finance.yahoo.com/quote/{tick}/balance-sheet/'.format(tick=self.ticker)
        isURL = 'https://finance.yahoo.com/quote/{tick}/financials/'.format(tick=self.ticker)
        ticker_info = {}
        ticker_info['IncomeStatement'] = scrap_url(isURL)
        ticker_info['BalanceSheet'] = scrap_url(bsURL)
        ticker_info['CashFlow'] = scrap_url(cfURL)
        return ticker_info
    
    def save_data(self, path:str = ''):
        """
        Save data to the specified or default arborescence registered during *Stock* construction

        :param path: Path to store data
        """

        if path != '':
            root, dirjson, dirsvg = create_arbo(path, self.ticker)
            self._arbo['path'] = root
            self._arbo['json']['path'] = dirjson
            self._arbo['svg']['path'] = dirsvg
            self._arbo['json']['filepath'] = dirjson + '/{}.json'.format(str.replace(self.ticker,'.','-'))
            self._arbo['svg']['filepath'] = dirsvg + '/{}.svg'.format(str.replace(self.ticker,'.','-'))

        self._yfdata.to_json(self._arbo['json']['filepath'])
        self._svg.write_image(self._arbo['svg']['filepath'],format='svg')

    def __stockprint__(self, string:str):
        print(f'Stock [{self.ticker}] : {string}')