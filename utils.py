import requests
import datetime as dt
import shutil
from bs4 import BeautifulSoup
import os

def scrap_url(URL: str):
    """
    Function to scrap financial data from `YahooFinance <https://finance.yahoo.com/>`_
    Works only for Louis' computer :)
    """

    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"}
    try:
        page = requests.get(URL,headers=headers)
    except:
        raise ConnectionRefusedError('Error, wrong agent or updated version of yfinance website')
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('div', {"class": "tableContainer yf-9ft13"})
    ticker_dict = {}
    for t in table:
        rows = t.find_all("div", {"class", "row lv-0 yf-t22klz"})
        for row in rows:
            str_row = row.get_text(separator="|").replace(" ","")
            str_row = str_row.replace('||',"|")
            list_row = str_row[1:].split("|")
            ticker_dict[list_row[0]] = list_row[1:]
    return ticker_dict

def create_arbo(path: str, name: str, date:dt.datetime, intraday:int = None):
    """
    Creates a data arborescence at the specified path

    :param path: Path of tbcreated dataset.
    :param name: Name of the dataset.
    :return: Directories addresses. *Root *Json *SVG
    """


    dirname = path + '/{}'.format(str.replace(name,'.','-'))
    dirnamedate = dirname + '/{}'.format(date)
    if intraday != None:
        dirnamedate+= f'_{intraday}'
    dirjson = dirnamedate + '/{}'.format('json')
    dirsvg = dirnamedate + '/{}'.format('svg')

    try:
        os.mkdir(dirname)
    except:
        pass

    dir_created = False

    try:
        os.mkdir(dirnamedate)
        os.mkdir(dirjson)
        os.mkdir(dirsvg)
        print('dinamedate1'+dirnamedate)
    except:
        pass
        

    return dirname, dirnamedate, dirjson, dirsvg 