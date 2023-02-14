import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as gr_obj
from plotly.subplots import make_subplots


def plot_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("History Stock Prices", "History Revenue"), vertical_spacing=.3)
    fig.add_trace(gr_obj.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.
                                 astype("float"), name="Stock Prices"), row=1, col=1)
    fig.add_trace(gr_obj.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True),
                                 y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Data", row=1, col=1)
    fig.update_xaxes(title_text="Data", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()


Tesla = yf.Ticker("TSLA")
Tesla_data = Tesla.history(period="max")
Tesla_data.reset_index(inplace=True)

url = " https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html5lib")

tables = soup.find_all('table')
for index,table in enumerate(tables):
    if "Tesla Quarterly Revenue" in str(table):
        table_index = index
tmp = [{"Date": "", "Revenue": ""}]
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if col:
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        tmp.append({"Date": Date, "Revenue": Revenue})
Tesla_revenue = pd.DataFrame.from_records(tmp)
Tesla_revenue = Tesla_revenue[Tesla_revenue['Revenue'] != ""]

plot_graph(Tesla_data, Tesla_revenue, 'Tesla')
