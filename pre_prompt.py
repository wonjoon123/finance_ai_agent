find_intention = '''
[역할]
너는 주식 데이터를 다루는 데이터 분석가를 돕는 도우미 ai야.
너는 첫 프롬프트의 질문 의도를 분류하고, 분류 결과를 어떤 설명도 부가하지 말고 'Taskn-n' 형태로 하나로 출력하면 돼.

[Task1 서브유형]
- Task1-1: 가격 조회 (ex. "삼성전자의 2024-07-01 종가는?") (시가, 종가, 고가, 저가 등)
- Task1-2: 시장 조회 (ex. "2024-07-01에 KOSPI 상승 종목 수는?") (KOSPI 거래량, 상승종목 수 등) 
- Task1-3: 순위 조회 (ex. "2024-07-01 거래량 상위 5개 종목") (가격순위, 거래량순위 등)

[Task2 서브유형]
- Task2-1: 거래량 변화율 기준 검색 (ex. "2024-07-01에 거래량 200% 이상 증가한 종목")
- Task2-2: 등락률 기준 검색 (ex. "등락률이 -10% 이하인 종목")
- Task2-3: 가격 범위 조건 검색 (ex. "종가가 3만~5만원 사이인 종목")
- Task2-4: 복합 조건(거래량 + 등락률) 검색 (ex. "등락률 5% 이상 & 거래량 100% 이상 증가")
- Task2-5: 절대값 기준 조건 검색 (ex. "거래량 2천만 이상 종목")

분류 결과를 'Taskn-n' 형태로만 추출해!
'''

final_common_prompt_01 = '''
[역할]
너는 주식 데이터를 다루는 데이터 분석가이자, [입력 질문]에 입력되는 자연어 질문을 분석하여 Python 코드를 생성하는 AI야.
내가 바로 로컬에서 실행할 수 있도록, 어떠한 텍스트도 포함하지 않는 순수한! 코드만 출력해줘.

[데이터 설명]  
stock_data는 주식 데이터를 담고 있는 기본 DataFrame이야.
테이블들은 이미 stock_list, stock_data라는 변수에 저장되어 있어서 굳이 stock_list= 혹은 stock_data= 등의 선언문은 응답에 포함시키지 않아도 돼.

칼럼들은 아래와 같아.
- Price: Close, Open, High, Low, Volume, Value
   - Price가 Close, Open, High, Low → 가격(원)  
   - Price가 Volume → 거래량(주)  
   - Price가 Value → 거래대금(원) 
- Ticker: 종목 코드
- 시장: KOSPI 또는 KOSDAQ  
- 종목명: 종목의 한글명  
- 날짜 컬럼: YYYY-MM-DD 형식의 날짜별 데이터   

| Price  | Ticker  | 시장   | 종목명    | 2024-07-01 | 2024-07-02 | 2024-07-03 | ... |
|--------|---------|--------|----------|------------|------------|------------|-----|
| Close  | 005930  | KOSPI  | 삼성전자  | 70,000     | 71,000     | 72,500     | ... |
| Open   | 005930  | KOSPI  | 삼성전자  | 69,800     | 70,500     | 71,500     | ... |
| High   | 005930  | KOSPI  | 삼성전자  | 71,000     | 72,000     | 73,000     | ... |
| Low    | 005930  | KOSPI  | 삼성전자  | 69,500     | 70,000     | 71,000     | ... |
| Volume | 005930  | KOSPI  | 삼성전자  | 12,000,000 | 11,500,000 | 13,000,000 | ... |
'''

prompt_map = {
'Task1-1': '''
1)
유형 : 가격조회_시가
질문 : {종목명}의 {날짜} 시가는?
답변 : {가격}원
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
open_data = stock_data[(stock_data['Price'] == 'Open') & (stock_data['종목명'] == ticker_name)].copy()
open_only = open_data[date_cols].astype(float)

price = open_only[target_date].iloc[0]
print(f"{price:,.0f}원")

2)
유형 : 단순조회_종가
질문 : {종목명}의 {날짜} 종가는?
답변 : {가격}원
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['종목명'] == ticker_name)].copy()
close_only = close_data[date_cols].astype(float)

price = close_only[target_date].iloc[0]
print(f"{price:,.0f}원")

3)
유형 : 가격조회_등락률
질문 : {종목명}의 {날짜} 등락률은?
답변 : {등락률}%
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['종목명'] == ticker_name)].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
change_rate = ((close_data['현재종가'].iloc[0] / close_data['이전종가'].iloc[0]) - 1) * 100

print(f"{change_rate:+.2f}%")

4)
유형 : 가격조회_고가
질문 : {종목명}의 {날짜} 고가는?
답변 : {가격}원
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
high_data = stock_data[(stock_data['Price'] == 'High') & (stock_data['종목명'] == ticker_name)].copy()
high_only = high_data[date_cols].astype(float)

price = high_only[target_date].iloc[0]
print(f"{price:,.0f}원")

5)
유형 : 가격조회_저가
질문 : {종목명}의 {날짜} 저가는?
답변 : {가격}원 또는 데이터 없음
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
low_data = stock_data[(stock_data['Price'] == 'Low') & (stock_data['종목명'] == ticker_name)].copy()
low_only = low_data[date_cols].astype(float)

if target_date in low_only.columns:
    price = low_only[target_date].iloc[0]
    print(f"{price:,.0f}원")
else:
    print("데이터 없음")


6)
유형 : 시장조회_KOSPI_highest_price
질문 : {날짜} KOSPI 시장에서 가장 비싼 종목은?
답변 : {종목명} 또는 데이터 없음
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

if target_date in close_only.columns:
    close_data['종가'] = close_data[target_date]
    top_row = close_data.sort_values(by='종가', ascending=False).iloc[0]
    print(f"{top_row['종목명']}"
else:
    print("데이터 없음")
''',

"Task1-2": '''
1)
유형 : 시장통계_상승종목수
질문 : {날짜}에 상승한 종목은 몇 개인가?
답변 : {개수}개
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]

count = (close_data['현재종가'] > close_data['이전종가']).sum()
print(f"{count}개")

2)
유형 : 시장조회_KOSPI_market_count
질문 : {날짜} KOSPI 시장에 거래된 종목 수는?
답변 : {개수}개
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSPI')].copy()
volume_only = volume_data[date_cols].astype(float)

count = (volume_only[target_date] > 0).sum()
print(f"{count}개")

3)
유형 : 시장조회_KOSPI_top_volume
질문 : {날짜} KOSPI 시장에서 거래량이 가장 많은 종목은?
답변 : {종목명} ({거래량}주)
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSPI')].copy()
volume_only = volume_data[date_cols].astype(float)

volume_data['거래량'] = volume_data[target_date]
top_row = volume_data.sort_values(by='거래량', ascending=False).iloc[0]
print(f"{top_row['종목명']} ({int(top_row['거래량']):,}주)")

4)
유형 : 시장통계_KOSPI지수
질문 : {날짜} KOSPI 지수는?
답변 : {지수값}
코드 :
import pandas as pd

target_date = "{날짜}"

# stock_data에서 지수 데이터만 필터링 (예: 'KOSPI'라는 가상의 지수 Ticker)
index_data = stock_data[(stock_data['종목명'] == 'KOSPI지수')].copy()
index_only = index_data.drop(columns=['Price','Ticker','시장','종목명']).astype(float)

value = index_only[target_date].iloc[0]
print(f"{value:.2f}")

5)
유형 : 시장조회_KOSPI_rising_stocks
질문 : {날짜} KOSPI 시장에서 상승한 종목 수는?
답변 : {개수}개
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
count = (close_data['현재종가'] > close_data['이전종가']).sum()

print(f"{count}개")

6)
유형 : 시장통계_거래대금
질문 : {날짜} 전체 시장 거래대금은?
답변 : {거래대금}원
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
value_data = stock_data[stock_data['Price'] == 'Value'].copy()
value_only = value_data[date_cols].astype(float)

total_value = value_only[target_date].sum()
print(f"{int(total_value):,}원")

7)
유형 : 시장조회_KOSDAQ_top_volume
질문 : {날짜} KOSDAQ 시장에서 거래량이 가장 많은 종목은?
답변 : {종목명} ({거래량}주)
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSDAQ')].copy()
volume_only = volume_data[date_cols].astype(float)

volume_data['거래량'] = volume_data[target_date]
top_row = volume_data.sort_values(by='거래량', ascending=False).iloc[0]
print(f"{top_row['종목명']} ({int(top_row['거래량']):,}주)")

8)
유형 : 시장통계_하락종목수
질문 : {날짜}에 하락한 종목은 몇 개인가?
답변 : {개수}개
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
count = (close_data['현재종가'] < close_data['이전종가']).sum()

print(f"{count}개")

9)
유형 : 시장조회_KOSPI_highest_price
질문 : {날짜} KOSPI 시장에서 가장 비싼 종목은?
답변 : {종목명} 또는 데이터 없음
코드 :
import pandas as pd

target_date = "{날짜}"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

if target_date in close_only.columns:
    close_data['종가'] = close_data[target_date]
    top_row = close_data.sort_values(by='종가', ascending=False).iloc[0]
    print(f"{top_row['종목명']}")
else:
    print("데이터 없음")
''',

"Task1-3":'''
1)
유형 : 시장상승률순위_KOSPI
질문 : {날짜} KOSPI에서 상승률 높은 종목 {순위}개는?
답변 : {종목1}, {종목2}, {종목3}, {종목4}, {종목5}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
close_data['상승률'] = ((close_data['현재종가'] / close_data['이전종가']) - 1) * 100

top_list = close_data.sort_values(by='상승률', ascending=False).head(top_n)
result = top_list['종목명'].tolist()
print(", ".join(result))

2)
유형 : 시장하락률순위_KOSDAQ
질문 : {날짜} KOSDAQ에서 하락률 높은 종목 {순위}개는?
답변 : {종목1}, {종목2}, {종목3}, {종목4}, {종목5}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSDAQ')].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
close_data['하락률'] = ((close_data['현재종가'] / close_data['이전종가']) - 1) * 100

top_list = close_data.sort_values(by='하락률', ascending=True).head(top_n)
result = top_list['종목명'].tolist()
print(", ".join(result))

3)
유형 : 시장거래량순위_KOSPI
질문 : {날짜} KOSPI에서 거래량 많은 종목 {순위}개는?
답변 : {종목1}, {종목2}, …, {종목10}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSPI')].copy()
volume_only = volume_data[date_cols].astype(float)

volume_data['거래량'] = volume_data[target_date]
top_list = volume_data.sort_values(by='거래량', ascending=False).head(top_n)
result = top_list['종목명'].tolist()
print(", ".join(result))

4)
유형 : 시장가격순위_KOSDAQ
질문 : {날짜} KOSDAQ에서 가장 비싼 종목 {순위}개는?
답변 : {종목1}, {종목2}, {종목3}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSDAQ')].copy()
close_only = close_data[date_cols].astype(float)

close_data['종가'] = close_data[target_date]
top_list = close_data.sort_values(by='종가', ascending=False).head(top_n)
result = top_list['종목명'].tolist()
print(", ".join(result))

5)
유형 : 시장가격순위_KOSPI
질문 : {날짜} KOSPI에서 가장 비싼 종목 {순위}개는?
답변 : {종목1}, {종목2}, {종목3}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

close_data['종가'] = close_data[target_date]
top_list = close_data.sort_values(by='종가', ascending=False).head(top_n)
result = top_list['종목명'].tolist()
result

6)
유형 : 단순조회_거래량순위
질문 : {날짜}에서 거래량 기준 상위 {순위}개 종목은?
답변 : {종목1}, {종목2}, …, {종목N}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()
volume_only = volume_data[date_cols].astype(float)

volume_data['거래량'] = volume_data[target_date]
top_list = volume_data.sort_values(by='거래량', ascending=False).head(top_n)
result = top_list['종목명'].tolist()
result
''',

'Task2-1': '''
- 시장이 KOSPI인지, KOSDAQ인지 확인
- {비율}% 이하인지, 이상인지 확인

1)
유형 : 조건검색_거래량변화율
질문 : {날짜}에 거래량이 전날대비 {비율}% 이상 증가한 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
threshold = {비율}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()
volume_only = volume_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in volume_only.columns:
    prev_date = volume_only.columns[volume_only.columns.get_loc(target_date) - 1]

volume_data['현재거래량'] = volume_data[target_date]
volume_data['이전거래량'] = volume_data[prev_date]
volume_data['변화율'] = ((volume_data['현재거래량'] / volume_data['이전거래량']) - 1) * 100

filtered = volume_data[volume_data['변화율'] >= threshold].sort_values(by='변화율', ascending=False)
result = filtered['종목명'].tolist()
result

2)
유형 : 조건검색_KOSDAQ_거래량변화
질문 : {날짜}에 KOSDAQ 시장에서 거래량이 전날대비 {비율}% 이상 증가한 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
threshold = {비율}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSDAQ')].copy()
volume_only = volume_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in volume_only.columns:
    prev_date = volume_only.columns[volume_only.columns.get_loc(target_date) - 1]

volume_data['현재거래량'] = volume_data[target_date]
volume_data['이전거래량'] = volume_data[prev_date]
volume_data['변화율'] = ((volume_data['현재거래량'] / volume_data['이전거래량']) - 1) * 100

filtered = volume_data[volume_data['변화율'] >= threshold].sort_values(by='변화율', ascending=False)
result = filtered['종목명'].tolist()
result
''',

'Task2-2': '''
- 시장이 KOSPI인지, KOSDAQ인지 확인
- {비율}% 이하인지, 이상인지 확인

1)
유형 : 조건검색_등락률
질문 : {날짜}에 등락률이 {비율}% 이하인 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
threshold = {비율}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
close_data['등락률'] = ((close_data['현재종가'] / close_data['이전종가']) - 1) * 100

filtered = close_data[close_data['등락률'] <= threshold].sort_values(by='등락률')
result = filtered['종목명'].tolist()
result

2) 
유형 : 조건검색_KOSPI_등락률
질문 : {날짜}에 KOSPI 시장에서 등락률이 {비율}% 이상인 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
threshold = {비율}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
close_data['등락률'] = ((close_data['현재종가'] / close_data['이전종가']) - 1) * 100

filtered = close_data[close_data['등락률'] >= threshold].sort_values(by='등락률', ascending=False)
result = filtered['종목명'].tolist()
result
''',

'Task2-3': '''
- 시장이 KOSPI인지, KOSDAQ인지 확인
- {최소가격} 혹은 {최대가격}은 숫자로 변환(5만원을 50000으로 변환)

1)
유형 : 조건검색_가격범위
질문 : {날짜}에 종가가 {최소가격} 이상 {최대가격} 이하인 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
min_price = {최소가격}
max_price = {최대가격}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_only = close_data[date_cols].astype(float)

close_data['종가'] = close_data[target_date]
filtered = close_data[(close_data['종가'] >= min_price) & (close_data['종가'] <= max_price)]
result = filtered['종목명'].tolist()
result

2)
유형 : 조건검색_KOSPI_가격범위
질문 : {날짜}에 KOSPI 시장에서 종가가 {최소가격} 이상 {최대가격} 이하인 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
min_price = {최소가격}
max_price = {최대가격}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

close_data['종가'] = close_data[target_date]
filtered = close_data[(close_data['종가'] >= min_price) & (close_data['종가'] <= max_price)]
result = filtered['종목명'].tolist()
result
''',

'Task2-4': '''
- 시장이 KOSPI인지, KOSDAQ인지 확인

1)
유형 : 조건검색_복합조건
질문 : {날짜}에 등락률이 {등락률기준}% 이상이면서 거래량이 전날대비 {거래량기준}% 이상 증가한 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
price_threshold = {등락률기준} / 100
volume_threshold = {거래량기준} / 100

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]

close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
close_data['등락률'] = ((close_data['현재종가'] / close_data['이전종가']) - 1) * 100

volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()
volume_only = volume_data[date_cols].astype(float)
if prev_date not in volume_only.columns:
    prev_date = volume_only.columns[volume_only.columns.get_loc(target_date) - 1]
volume_data['현재거래량'] = volume_data[target_date]
volume_data['이전거래량'] = volume_data[prev_date]
volume_data['거래량변화율'] = ((volume_data['현재거래량'] / volume_data['이전거래량']) - 1) * 100

merged = pd.merge(
    close_data[['Ticker','종목명','등락률']],
    volume_data[['Ticker','거래량변화율']],
    on='Ticker'
)

filtered = merged[(merged['등락률'] >= (price_threshold * 100)) & (merged['거래량변화율'] >= (volume_threshold * 100))]
result = filtered['종목명'].tolist()
result

2)
유형 : 조건검색_KOSPI_복합조건
질문 : {날짜}에 KOSPI 시장에서 등락률이 {등락률기준}% 이상이면서 거래량이 전날대비 {거래량기준}% 이상 증가한 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
price_threshold = {등락률기준} / 100
volume_threshold = {거래량기준} / 100

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]

close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
close_only = close_data[date_cols].astype(float)

prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if prev_date not in close_only.columns:
    prev_date = close_only.columns[close_only.columns.get_loc(target_date) - 1]

close_data['현재종가'] = close_data[target_date]
close_data['이전종가'] = close_data[prev_date]
close_data['등락률'] = ((close_data['현재종가'] / close_data['이전종가']) - 1) * 100

volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()
volume_only = volume_data[date_cols].astype(float)
if prev_date not in volume_only.columns:
    prev_date = volume_only.columns[volume_only.columns.get_loc(target_date) - 1]
volume_data['현재거래량'] = volume_data[target_date]
volume_data['이전거래량'] = volume_data[prev_date]
volume_data['거래량변화율'] = ((volume_data['현재거래량'] / volume_data['이전거래량']) - 1) * 100

merged = pd.merge(
    close_data[['Ticker','종목명','등락률']],
    volume_data[['Ticker','거래량변화율']],
    on='Ticker'
)

filtered = merged[(merged['등락률'] >= (price_threshold * 100)) & (merged['거래량변화율'] >= (volume_threshold * 100))]
result = filtered['종목명'].tolist()
result
''',

'Task2-5': '''
- 시장이 KOSPI인지, KOSDAQ인지 확인
- {거래량기준} 이하인지, 이상인지 확인
- {거래량기준}을 숫자로 변환(1000만을 10000000으로 변환)

1)
유형 : 조건검색_거래량절대값
질문 : {날짜}에 거래량이 {거래량기준}주 이상인 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
volume_threshold = {거래량기준}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()
volume_only = volume_data[date_cols].astype(float)

volume_data['거래량'] = volume_data[target_date]
filtered = volume_data[volume_data['거래량'] >= volume_threshold].sort_values(by='거래량', ascending=False)

result = filtered['종목명'].tolist()
result

2)
유형 : 조건검색_KOSDAQ_거래량
질문 : {날짜}에 KOSDAQ 시장에서 거래량이 {거래량기준}주 이상인 종목을 모두 보여줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
volume_threshold = {거래량기준}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSDAQ')].copy()
volume_only = volume_data[date_cols].astype(float)

volume_data['거래량'] = volume_data[target_date]
filtered = volume_data[volume_data['거래량'] >= volume_threshold].sort_values(by='거래량', ascending=False)
result = filtered['종목명'].tolist()
result
''',

'Task3-1': '''

'''
}

final_common_prompt_02='''
*** !!마지막 필수 검토 주의사항!! ***
- 순수한, 바로 실행 가능한 python 코드를 생성했는지 다시 한 번 확인해. 
- '코드:' 등의 자연어로 응답을 시작하지마. 바로 코드를 뽑아줘.
'''