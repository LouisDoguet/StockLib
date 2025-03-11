Import library :

import StockLib as sl will get you 2 main objects :

sl.Stock() -> Stock object
Methods : dowload, savedata, plotcandle ...

sl.StockBundle -> Bundle, group of stocks
Possible to plot everything w plotcandles


Notes from Baptiste:
- Get info from other sources (Alpha Vantage, Bloomberg, etc)
- SQL storage for stocks info (PostgreSQL, MySQL ou NoSQL MongoDB, InfluxDB)
- SMA (Moyenne Mobile Simple), EMA (MM exponentielle) et Golden/Death Cross pour les moyennes mobiles {MM}. Des Indicateurs de Tendances (IT) ADX (average direction index), Ichimoku Kinko Hyo et Parabolic SAR (discutable). De Momentum RSI, MACD, Stochastic Oscillator. Indicateur de Volume avec l'on-balance Volume (OBV) et le Volume Weighted Average Price (VWAP). Aussi des indicateur de résistence.
