import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def make_graph(stock_data, revenue_data, stock):
    fig=make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=0.3)
    
    stock_data['Date']=pd.to_datetime(stock_data['Date']).dt.tz_localize(None)
    revenue_data['Date']=pd.to_datetime(revenue_data['Date'])
    
    three_years_ago=datetime.now()-timedelta(days=3*365)
    stock_data_specific=stock_data[stock_data['Date'] >= three_years_ago]
    revenue_data_specific=revenue_data[revenue_data['Date'] >= three_years_ago]
    
    fig.add_trace(go.Scatter(x=stock_data_specific['Date'], y=stock_data_specific['Close'].astype(float), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=revenue_data_specific['Date'], y=revenue_data_specific['Revenue'].astype(float), name="Revenue"), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )
    fig.show()

#Input ticker symbol
ticker=input("Enter Ticker: ").upper()
stock=yf.Ticker(ticker)
start_date=(datetime.now()-timedelta(days=3*365)).strftime('%Y-%m-%d')
end_date=datetime.now().strftime('%Y-%m-%d')
stock_data=stock.history(start=start_date, end=end_date)
stock_data.reset_index(inplace=True)

#Print first few rows of stock data
print(stock_data.head())

#Get revenue data from Yahoo Finance
financials=stock.quarterly_financials.T
financials.reset_index(inplace=True)
financials.rename(columns={'index': 'Date', 'Total Revenue': 'Revenue'}, inplace=True)

#Filter to get the most recent 3 years of data
financials['Date']=pd.to_datetime(financials['Date'])
revenue_data=financials[financials['Date'] >= datetime.now()-timedelta(days=3*365)]
revenue_data=revenue_data[['Date', 'Revenue']]

#Print last few rows of revenue data
print(revenue_data.tail())

#Make a graph
make_graph(stock_data, revenue_data, ticker)
