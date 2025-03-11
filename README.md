Import library :

import StockLib as sl will get you 2 main objects :

sl.Stock() -> Stock object
Methods : dowload, savedata, plotcandle ...

sl.StockBundle -> Bundle, group of stocks
Possible to plot everything w plotcandles


Notes from Baptiste:
- Get info from other sources (Alpha Vantage, Bloomberg, etc)
- SQL storage for stocks info (PostgreSQL, MySQL ou NoSQL MongoDB, InfluxDB)
