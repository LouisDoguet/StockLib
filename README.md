# 📊 StockLib

![newplot](https://github.com/user-attachments/assets/a17e52f0-e51e-4e8d-b715-91052d9dbda7)


StockLib is a Python library designed to manipulate and analyze stock market data. (In development) It will include functionalities to retrieve, visualize, and analyze financial data, particularly for creating interactive plots using **Plotly**.

## 🚀 Features (projected)

- Retrieve stock market data (e.g., historical prices)
- Display interactive charts with **Plotly**
- Basic and advanced technical analysis
- Support for OHLC data (Open, High, Low, Close)

## 🔧 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/LouisDoguet/StockLib.git
    ```
   
2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Linux/macOS
    env\Scripts\activate     # On Windows
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 📈 Example Usage

Here's an example of how to load data and plot a chart using **Plotly**:

```python
import StockLib as sl

tickers = ['GOOG','AAPL','MSFT','TSLA','F','NVDA']
bun = sl.Bundle(tickers)
bun.download(
    period='1d',
    interval='1m',
    overwrite=True
)
bun.plotcandle()
```
