import pandas as pd
from pykrx import stock
import sqlite3


df_kospi = stock.get_market_ticker_list(market="KOSPI")
df_kosdaq = stock.get_market_ticker_list(market="KOSDAQ") 

stock_list = []

for code in df_kospi:
    name = stock.get_market_ticker_name(code)
    stock_list.append({"종목코드": code, "종목명": name, '시장': 'KOSPI'})

for code in df_kosdaq:
    name = stock.get_market_ticker_name(code)
    stock_list.append({"종목코드": code, "종목명": name, '시장': 'KOSDAQ'})

stock_df = pd.DataFrame(stock_list)

stock_df['yfinance_ticker'] = stock_df.apply(lambda row: row['종목코드'] + '.KS' if row['시장'] == 'KOSPI' else row['종목코드'] + '.KQ', axis=1)

### finance.db에 stock_list 라는 이름의 table을 저장
conn = sqlite3.connect('finance.db')
stock_df.to_sql('stock_list', conn, if_exists='replace', index=False)
conn.close()