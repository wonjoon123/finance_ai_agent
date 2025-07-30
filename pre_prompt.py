find_intention = '''
[역할]  
너는 주식 데이터를 다루는 데이터 분석가를 돕는 도우미 AI야.  
입력된 질문의 의도를 분석하고, 그 결과를 **설명 없이** `'Taskn-n'` 형식으로 하나만 출력해.  
{날짜}, {거래량기준}, {비율}, {종목}과 같은 정확한 정보가 없을 경우에는 Task4 중 하나로 분류해줘.

---

## 우선 분류 규칙 (매우 중요)
1. **질문에 아래 중 하나라도 없다면 무조건 Task4로 분류한다.**
   - 날짜(예: "2024-07-01" 형식 또는 "7월 1일" 등 구체 날짜)
   - 종목명(예: "삼성전자", "현대차" 등 특정 기업명)
   - 명확한 기준 수치(예: "5% 이상", "2천만 주 이상" 등)
2. **모호성 유형에 따라 Task4 세부 유형을 선택한다.**
   - 날짜가 모호 → Task4-1
   - 종목명이 모호 → Task4-2
   - 기준 수치가 모호 → Task4-3
   - 위 2개 이상이 모호 → Task4-4
3. 위 조건이 모두 충족되면 Task1~3 규칙으로 분류한다.

---

## 분류 기준

### Task4 : 모호한 질문 해석  
- **Task4-1** : 날짜가 명확하지 않은 경우  
  예) `"최근, 지난 겨울, 요즘 등 정확한 날짜가 아닌 시간을 표현하는 말"`  
- **Task4-2** : 종목명이 명확하지 않은 경우  
  예) `"좋은 2차전지 주식 알려줘", "반도체 관련 종목 뭐 있어?" 등 특정 종목명이 없는 질문"`  
- **Task4-3** : 수치나 조건이 모호한 경우  
  예) `"많이 떨어진 주식", "비싸지 않은 종목" 등 기준 수치가 명확하지 않은 질문"`  
- **Task4-4** : 위 조건이 2개 이상 혼합되어 매우 모호한 경우  
  예) `"요즘 괜찮은 종목 뭐 있어?", "가치주 중 좋은 것 추천해줘"`

### Task1 : 단순 조회  
- **Task1-1** : 가격 조회  
  예) `"삼성전자의 2024-07-01 종가는?"` (시가, 종가, 고가, 저가 등)  
- **Task1-2** : 시장 조회  
  예) `"2024-07-01에 KOSPI 상승 종목 수는?"` (KOSPI 거래량, 상승 종목 수 등)  
- **Task1-3** : 순위 조회  
  예) `"2024-07-01 거래량 상위 5개 종목"` (가격 순위, 거래량 순위 등)

### Task2 : 조건 검색  
- **Task2-1** : 거래량 변화율 기준 검색  
  예) `"2024-07-01에 거래량 200% 이상 증가한 종목"`  
- **Task2-2** : 등락률 기준 검색  
  예) `"등락률이 -10% 이하인 종목"`  
- **Task2-3** : 가격 범위 조건 검색  
  예) `"종가가 3만~5만원 사이인 종목"`  
- **Task2-4** : 복합 조건 검색 (거래량 + 등락률)  
  예) `"등락률 5% 이상 & 거래량 100% 이상 증가"`  
- **Task2-5** : 절대값 기준 조건 검색  
  예) `"거래량 2천만 이상 종목"`

### Task3 : 시그널 감지  
- **Task3-1** : 특정 일수 이동평균(MA) 돌파 감지  
  예) `"종가가 20일 이동평균보다 10% 이상 높은 종목"`  
- **Task3-2** : RSI 과매수/과매도 감지  
  예) `"RSI가 70 이상인 과매수 종목"`  
- **Task3-3** : 볼린저 밴드 하단/상단 터치 감지  
  예) `"볼린저 밴드 하단에 터치한 종목"`  
- **Task3-4** : 일정 기간 크로스 발생 종목 감지  
  예) `"데드크로스가 발생한 종목"`  
- **Task3-5** : 일정 기간 크로스 발생 횟수 감지  
  예) `"골든크로스가 몇 번 발생"`  
- **Task3-6** : 거래량 급증 감지  
  예) `"거래량이 20일 평균 대비 500% 이상 급증한 종목"`  

---

## 출력 규칙
- **반드시** `'Taskn-n'` 형식으로만 출력 (설명, 부가 텍스트 금지)
'''

final_common_prompt = '''
[역할]  
너는 주식 데이터를 다루는 데이터 분석가이자, [입력 질문]에 대한 **Python 코드**를 생성하는 AI야.  
**로컬에서 바로 실행할 수 있도록, 설명이나 텍스트 없이 오직 순수한 코드만 출력해야 해.**
단, Task4에 포함될 때에는 코드 출력이 아니라 각 서브 유형에 맞는 자연어 답변을 출력해야 해.

[필수 검토 주의사항]
- 문자열 출력 시 다음 포맷을 준수해야 한다:
  - 정수형: `print(f"{price:,.0f}원")`  
  - 소수점 둘째 자리까지 필요할 때: `print(f"{price:,.2f}원")`  
- 토요일·일요일(주말)에는 데이터가 없을 수 있다는 점을 고려해야 한다.

---

## 데이터 설명
- **DataFrame**: `stock_data` (기본 주식 데이터)  
- **이미 존재하는 변수**: `stock_list`, `stock_data`  
  → 코드에서 별도 선언(`stock_list = ...`, `stock_data = ...`)은 포함하지 않는다.  

### 칼럼 구조
- **Price**: `"Close"`, `"Open"`, `"High"`, `"Low"`, `"Volume"`, `"Value"`  
  - `"Close"`, `"Open"`, `"High"`, `"Low"` → 가격(원)  
  - `"Volume"` → 거래량(주)  
  - `"Value"` → 거래대금(원)  
- **Ticker**: 종목 코드
- **시장**: `"KOSPI"` 또는 `"KOSDAQ"`  
- **종목명**: 종목 한글명
- **날짜 컬럼**: `YYYY-MM-DD` 형식 (예: `"2024-07-01"`)

| Price  | Ticker  | 시장   | 종목명    | 2024-07-01 | 2024-07-02 | 2024-07-03 | ... |
|--------|---------|--------|----------|------------|------------|------------|-----|
| Close  | 005930  | KOSPI  | 삼성전자  | 70,000     | 71,000     | 72,500     | ... |
| Open   | 005930  | KOSPI  | 삼성전자  | 69,800     | 70,500     | 71,500     | ... |
| High   | 005930  | KOSPI  | 삼성전자  | 71,000     | 72,000     | 73,000     | ... |
| Low    | 005930  | KOSPI  | 삼성전자  | 69,500     | 70,000     | 71,000     | ... |
| Volume | 005930  | KOSPI  | 삼성전자  | 12,000,000 | 11,500,000 | 13,000,000 | ... |
'''

prompt_map = {
"Task4-1": """
원질문: '{원질문}'
출력: "몇 월 며칠 기준으로 결과를 알고 싶으신가요?"
""",

"Task4-2": """
원질문: '{원질문}'
출력: "어떤 종목(회사명)을 말씀하시는 건가요?"
""",

"Task4-3": """
원질문: '{원질문}'
출력: "몇 퍼센트 이상(또는 몇 주 이상)으로 기준을 잡고 싶으신가요?"
""",

"Task4-4": """
원질문: '{원질문}'
출력: "어느 날짜 기준으로 어떤 종목(또는 조건)을 찾고 싶으신가요?"
""",

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
import yfinance as yf
import pandas as pd

target_date = "{날짜}"

# KOSPI 지수는 ^KS11, KOSDAQ 지수는 ^KQ11
kospi = yf.Ticker("^KS11")
kosdaq = yf.Ticker("^KQ11")

df = kospi.history(period="2y")

try:
    close_price = df.loc[target_date]["Close"]
    print(f"{close_price:.2f}")
except:
    print('해당 날짜에 존재하는 데이터가 없습니다.')

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

volume_data = stock_data[stock_data['Price'] == 'Volume'][['Ticker', target_date]].copy()
volume_data = volume_data.rename(columns={target_date: 'Volume'})

close_data = stock_data[stock_data['Price'] == 'Close'][['Ticker', target_date]].copy()
close_data = close_data.rename(columns={target_date: 'Close'})

final_data = pd.merge(volume_data, close_data, on='Ticker')

final_data["거래대금"] = final_data["Volume"] * final_data["Close"]
total_turnover = final_data["거래대금"].sum()

print(f"{total_turnover:,.0f}원")

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

try:
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
except KeyError:
    print("해당 날짜 데이터 없음")

2)
유형 : 시장하락률순위_KOSDAQ
질문 : {날짜} KOSDAQ에서 하락률 높은 종목 {순위}개는?
답변 : {종목1}, {종목2}, {종목3}, {종목4}, {종목5}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

try:
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
except KeyError:
    print("해당 날짜 데이터 없음")

3)
유형 : 시장거래량순위_KOSPI
질문 : {날짜} KOSPI에서 거래량 많은 종목 {순위}개는?
답변 : {종목1}, {종목2}, …, {종목10}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

try:
    date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
    volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSPI')].copy()
    volume_only = volume_data[date_cols].astype(float)

    volume_data['거래량'] = volume_data[target_date]
    top_list = volume_data.sort_values(by='거래량', ascending=False).head(top_n)
    result = top_list['종목명'].tolist()
    print(", ".join(result))
except KeyError:
    print("해당 날짜 데이터 없음")

4)
유형 : 시장가격순위_KOSDAQ
질문 : {날짜} KOSDAQ에서 가장 비싼 종목 {순위}개는?
답변 : {종목1}, {종목2}, {종목3}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

try:
    date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
    close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSDAQ')].copy()
    close_only = close_data[date_cols].astype(float)

    close_data['종가'] = close_data[target_date]
    top_list = close_data.sort_values(by='종가', ascending=False).head(top_n)
    result = top_list['종목명'].tolist()
    print(", ".join(result))
except KeyError:
    print("해당 날짜 데이터 없음")

5)
유형 : 시장가격순위_KOSPI
질문 : {날짜} KOSPI에서 가장 비싼 종목 {순위}개는?
답변 : {종목1}, {종목2}, {종목3}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

try:
    date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
    close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['시장'] == 'KOSPI')].copy()
    close_only = close_data[date_cols].astype(float)

    close_data['종가'] = close_data[target_date]
    top_list = close_data.sort_values(by='종가', ascending=False).head(top_n)
    result = top_list['종목명'].tolist()
    print(", ".join(result))
except KeyError:
    print("해당 날짜 데이터 없음")

6)
유형 : 단순조회_거래량순위
질문 : {날짜}에서 거래량 기준 상위 {순위}개 종목은?
답변 : {종목1}, {종목2}, …, {종목N}
코드 :
import pandas as pd

target_date = "{날짜}"
top_n = {순위}

try:
    date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
    volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()
    volume_only = volume_data[date_cols].astype(float)

    volume_data['거래량'] = volume_data[target_date]
    top_list = volume_data.sort_values(by='거래량', ascending=False).head(top_n)
    result = top_list['종목명'].tolist()
    print(", ".join(result))
except KeyError:
    print("해당 날짜 데이터 없음")
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
print(result)

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
print(result)
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
print(result)

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
print(result)
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
print(result)

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
print(result)
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
print(result)

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
print(result)
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
print(result)

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
print(result)
''',

'Task3-1': '''
1)
유형 : 시그널감지_MA20돌파
질문 : {날짜}에 종가가 20일 이동평균보다 {비율}% 이상 높은 종목을 알려줘
답변 : {종목1}({비율1}%), {종목2}({비율2}%), …
코드 :
import pandas as pd

target_date = "{날짜}"
threshold = {비율} / 100
window = 20

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_data = close_data.set_index('Ticker')
close_only = close_data[date_cols].astype(float)

ma20 = close_only.T.rolling(window=window, min_periods=window).mean().T
ratio = ((close_only[target_date] / ma20[target_date]) - 1) * 100

filtered = ratio[ratio >= (threshold * 100)].sort_values(ascending=False)
result = [f"{close_data.loc[ticker, '종목명']}({ratio[ticker]:.2f}%)" for ticker in filtered.index]
print(result)

2)
유형 : 시그널감지_MA60돌파
질문 : {날짜}에 종가가 60일 이동평균보다 {비율}% 이상 높은 종목을 알려줘
답변 : {종목1}({비율1}%), {종목2}({비율2}%), …
코드 :
import pandas as pd

target_date = "{날짜}"
threshold = {비율} / 100
window = 60

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_data = close_data.set_index('Ticker')
close_only = close_data[date_cols].astype(float)

ma60 = close_only.T.rolling(window=window, min_periods=window).mean().T
ratio = ((close_only[target_date] / ma60[target_date]) - 1) * 100

filtered = ratio[ratio >= (threshold * 100)].sort_values(ascending=False)
result = [f"{close_data.loc[ticker, '종목명']}({ratio[ticker]:.2f}%)" for ticker in filtered.index]
print(result)
''',

'Task3-2': '''
1)
유형 : 시그널감지_RSI_과매수
질문 : {날짜}에 RSI가 {수치} 이상인 과매수 종목을 알려줘
답변 : {종목1}(RSI:{값1}), {종목2}(RSI:{값2}), …
코드 : 
import pandas as pd
import numpy as np

def calculate_rsi_vectorized(df_close, period=14):
    delta = df_close.diff(axis=1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    gain_ma = pd.DataFrame(gain, index=df_close.index, columns=df_close.columns).rolling(window=period, axis=1).mean()
    loss_ma = pd.DataFrame(loss, index=df_close.index, columns=df_close.columns).rolling(window=period, axis=1).mean()
    rs = gain_ma / loss_ma
    rsi = 100 - (100 / (1 + rs))
    return rsi

target_date = "{날짜}"
threshold = {수치}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].set_index('Ticker')
close_only = close_data[date_cols].astype(float)

rsi_df = calculate_rsi_vectorized(close_only)
filtered = rsi_df[rsi_df[target_date] >= threshold]

result = [
    f"{close_data.loc[ticker, '종목명']} (RSI:{rsi_df.loc[ticker, target_date]:.1f})"
    for ticker in filtered.index
]
print(result)

2)
유형 : 시그널감지_RSI_과매도
질문 : {날짜}에 RSI가 {수치} 이하인 과매도 종목을 알려줘
답변 : {종목1}(RSI:{값1}), {종목2}(RSI:{값2}), …
코드 :
import pandas as pd
import numpy as np

def calculate_rsi_vectorized(df_close, period=14):
    delta = df_close.diff(axis=1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    gain_ma = pd.DataFrame(gain, index=df_close.index, columns=df_close.columns).rolling(window=period, axis=1).mean()
    loss_ma = pd.DataFrame(loss, index=df_close.index, columns=df_close.columns).rolling(window=period, axis=1).mean()
    rs = gain_ma / loss_ma
    rsi = 100 - (100 / (1 + rs))
    return rsi

target_date = "{날짜}"
threshold = {수치}

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].set_index('Ticker')
close_only = close_data[date_cols].astype(float)

rsi_df = calculate_rsi_vectorized(close_only)
filtered = rsi_df[rsi_df[target_date] <= threshold]

result = [
    f"{close_data.loc[ticker, '종목명']}(RSI:{rsi_df.loc[ticker, target_date]:.1f})"
    for ticker in filtered.index
]
print(result)
''',

'Task3-3': '''
1)
유형 : 시그널감지_볼린저_lower
질문 : {날짜}에 볼린저 밴드 하단에 터치한 종목을 알려줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
window = 20
num_std = 2

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_data = close_data.set_index('Ticker')
close_only = close_data[date_cols].astype(float)

rolling_mean = close_only.T.rolling(window=window).mean().T
rolling_std = close_only.T.rolling(window=window).std().T
lower_band = rolling_mean - (rolling_std * num_std)

touch_lower = close_only[target_date] <= lower_band[target_date]
filtered = close_only[touch_lower]

result = [close_data.loc[ticker, '종목명'] for ticker in filtered.index]
print(result)

2)
유형 : 시그널감지_볼린저_upper
질문 : {날짜}에 볼린저 밴드 상단에 터치한 종목을 알려줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

target_date = "{날짜}"
window = 20
num_std = 2

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
close_data = close_data.set_index('Ticker')
close_only = close_data[date_cols].astype(float)

rolling_mean = close_only.T.rolling(window=window).mean().T
rolling_std = close_only.T.rolling(window=window).std().T
upper_band = rolling_mean + (rolling_std * num_std)

touch_upper = close_only[target_date] >= upper_band[target_date]
filtered = close_only[touch_upper]

result = [close_data.loc[ticker, '종목명'] for ticker in filtered.index]
print(result)
''',

'Task3-4': '''
1)
유형 : 시그널종목_데드크로스_기간
질문 : {시작일}부터 {종료일}까지 데드크로스가 발생한 종목을 알려줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 : 
import pandas as pd

start_date = "{시작일}"
end_date = "{종료일}"
short_window = 20
long_window = 60

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()

result = []

for _, row in close_data.iterrows():
    ticker = row['Ticker']
    name = row['종목명']
    close_series = row[date_cols].astype(float)
    close_series.index = pd.to_datetime(date_cols)

    ma_short = close_series.rolling(window=short_window).mean()
    ma_long = close_series.rolling(window=long_window).mean()

    dead_cross = (ma_short < ma_long) & (ma_short.shift(1) >= ma_long.shift(1))

    mask = (close_series.index >= start_date) & (close_series.index <= end_date)
    if dead_cross[mask].any():
        result.append(name)

print(result)

2)
유형 : 시그널종목_골든크로스_기간
질문 : {시작일}부터 {종료일}까지 골든크로스가 발생한 종목을 알려줘
답변 : {종목1}, {종목2}, {종목3}, …
코드 :
import pandas as pd

start_date = "{시작일}"
end_date = "{종료일}"
short_window = 20
long_window = 60

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data = stock_data[stock_data['Price'] == 'Close'].copy()

result = []

for _, row in close_data.iterrows():
    name = row['종목명']
    close_series = row[date_cols].astype(float)
    close_series.index = pd.to_datetime(date_cols)

    ma_short = close_series.rolling(window=short_window).mean()
    ma_long = close_series.rolling(window=long_window).mean()

    golden_cross = (ma_short > ma_long) & (ma_short.shift(1) <= ma_long.shift(1))

    mask = (close_series.index >= start_date) & (close_series.index <= end_date)
    if golden_cross[mask].any():
        result.append(name)

print(result)
''',

'Task3-5': '''
1)
유형 : 시그널횟수_골든크로스
질문 : {종목명}에서 {시작일}부터 {종료일}까지 골든크로스가 몇 번 발생했어?
답변 : {횟수}번
코드 :
import pandas as pd

ticker_name = "{종목명}"
start_date = "{시작일}"
end_date = "{종료일}"
short_window = 20
long_window = 60

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
row = stock_data[(stock_data['Price'] == 'Close') & (stock_data['종목명'] == ticker_name)]

close_series = row[date_cols].iloc[0].astype(float)
close_series.index = pd.to_datetime(date_cols)


ma_short = close_series.rolling(window=short_window).mean()
ma_long = close_series.rolling(window=long_window).mean()

golden_cross = (ma_short > ma_long) & (ma_short.shift(1) <= ma_long.shift(1))

mask = (close_series.index >= start_date) & (close_series.index <= end_date)
count = golden_cross[mask].sum()

result = f"{count}번"
print(result)

2)
유형 : 시그널횟수_데드크로스
질문 : {종목명}에서 {시작일}부터 {종료일}까지 데드크로스가 몇 번 발생했어?
답변 : {횟수}번
코드 :
import pandas as pd

ticker_name = "{종목명}"
start_date = "{시작일}"
end_date = "{종료일}"
short_window = 20
long_window = 60

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
row = stock_data[(stock_data['Price'] == 'Close') & (stock_data['종목명'] == ticker_name)]

close_series = row[date_cols].iloc[0].astype(float)
close_series.index = pd.to_datetime(date_cols)

ma_short = close_series.rolling(window=short_window).mean()
ma_long = close_series.rolling(window=long_window).mean()

dead_cross = (ma_short < ma_long) & (ma_short.shift(1) >= ma_long.shift(1))

mask = (close_series.index >= start_date) & (close_series.index <= end_date)
count = dead_cross[mask].sum()

result = f"{count}번"
print(result)

3)
유형 : 시그널횟수_크로스_통합
질문 : {종목명}이(가) {시작일}부터 {종료일}까지 데드크로스 또는 골든크로스가 몇 번 발생했어?
답변 : 데드크로스 {데드크로스횟수}번, 골든크로스 {골든크로스횟수}번
코드 :
import pandas as pd

ticker_name = "{종목명}"
start_date = "{시작일}"
end_date = "{종료일}"
short_window = 20
long_window = 60

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
row = stock_data[(stock_data['Price'] == 'Close') & (stock_data['종목명'] == ticker_name)]

close_series = row[date_cols].iloc[0].astype(float)
close_series.index = pd.to_datetime(date_cols)

ma_short = close_series.rolling(window=short_window).mean()
ma_long = close_series.rolling(window=long_window).mean()

golden_cross = (ma_short > ma_long) & (ma_short.shift(1) <= ma_long.shift(1))
dead_cross = (ma_short < ma_long) & (ma_short.shift(1) >= ma_long.shift(1))

mask = (close_series.index >= start_date) & (close_series.index <= end_date)
golden_count = golden_cross[mask].sum()
dead_count = dead_cross[mask].sum()

result = f"데드크로스 {dead_count}번, 골든크로스 {golden_count}번"
print(result)
''',

'Task3-6': '''
유형 : 시그널감지_거래량급증
질문 : {날짜}에 거래량이 {기간}일 평균 대비 {비율}% 이상 급증한 종목을 알려줘
답변 : {종목1}({비율1}%), {종목2}({비율2}%), …
코드 :
import pandas as pd

target_date = "{날짜}"
rolling_window = "{기간}"
threshold = "{비율}" / 100

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()
volume_only = volume_data[date_cols].astype(float)
ma = volume_only.T.rolling(window=rolling_window, min_periods=rolling_window).mean().T

volume_data['거래량'] = volume_data[target_date]
volume_data['MA'] = ma[target_date]

filtered = volume_data[volume_data['거래량'] >= volume_data['MA'] * (1 + threshold)].copy()
filtered['증가율'] = ((filtered['거래량'] / filtered['MA']) - 1) * 100
filtered = filtered.sort_values(by='증가율', ascending=False)

# NaN 제거
filtered = filtered[filtered['증가율'].notna()]

result = filtered.apply(lambda row: f"{row['종목명']}({row['증가율']:.0f}%)", axis=1)
print(result.tolist())
'''
}