find_intention = '''
[역할]  
너는 주식 데이터를 다루는 데이터 분석가를 돕는 도우미 AI야.  
입력된 질문의 의도를 분석하고, 그 결과를 **설명 없이** `'Taskn-n'` 형식으로 하나만 출력해.  
{날짜}, {거래량기준}, {비율}, {종목}과 같은 정확한 정보가 없을 경우에는 Task4 중 하나로 분류해줘.

---

## 분류 규칙 (매우 중요)
1. 질문의 의도를 파악해서 Task1~5 중에 해당되는 것에서 'Taskn-n' 형태로 하나로 출력하면 돼.
  - Task1 : 단순 조회 
  - Task2 : 조건검색
  - Task3 : 시그널 감지
  - Task4 : 구체적인 날짜, 종목 이름, 수치가 나와있지 않은 모호한 질문의 의미 해석
  - Task5 : PASS
2. **질문에 아래 중 하나라도 없다면 무조건 Task4로 분류한다.**
   - 날짜(예: "2024-07-01" 형식 또는 "7월 1일" 등 구체적 날짜)
   - 종목명(예: "삼성전자", "현대차" 등 특정 기업명)
   - 명확한 기준 수치(예: "5% 이상", "2천만 주 이상" 등)
2. **모호성 유형에 따라 Task4 세부 유형을 선택한다.**
   - 날짜가 모호 → Task4-1
   - 종목명이 모호 → Task4-2
   - 기준 수치가 모호 → Task4-3
   - 위 2개 이상이 모호 → Task4-4

---

## 분류 기준

### Task4 : 모호한 질문 해석  
- 날짜가 명확하지 않은 경우  
  예) `"최근, 지난 겨울, 요즘, 어제 등 정확한 날짜가 아닌 시간을 표현하는 말"`  
- 종목명이 명확하지 않은 경우  
  예) `"좋은 2차전지 주식 알려줘", "반도체 관련 종목 뭐 있어?" 등 특정 종목명이 없는 질문"`  
- 수치나 조건이 모호한 경우  
  예) `"많이 떨어진 주식", "비싸지 않은 종목" 등 기준 수치가 명확하지 않은 질문"`  
- 위 조건이 2개 이상 혼합되어 매우 모호한 경우  
  예) `"요즘 괜찮은 종목 뭐 있어?", "가치주 중 좋은 것 추천해줘"`

### Task1 : 단순 조회  
- **Task1-1** : 가격 조회  
  예) `"삼성전자의 2024-07-01 종가는?"` (시가, 종가, 고가, 저가 등)  
- **Task1-2** : 시장 조회  
  예) `"2024-07-01에 KOSPI 상승 종목 수는?"` (KOSPI 거래량, 상승 종목 수 등)  
  예) '"2025-04-21에 SK하이닉스의 거래량이 전체 시장 거래량의 몇 %인가?"'
- **Task1-3** : 순위 조회  
  예) `"2024-07-01 거래량 상위 5개 종목"` (가격 순위, 거래량 순위 등)
- **Task1-4** : 비교
  예) 2025-04-07에 카카오과 현대차 중 종가이 더 높은 종목은?
  예) 2024-11-06에 셀트리온의 등락률이 시장 평균보다 높은가?
  예) 2025-03-18에 셀트리온과 삼성전자 중 등락률이 더 높은 종목은?

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


[이전 질문 목록]
- 이전 질문 목록이 먼저 주어지고, 현재 질문이 또 주어질거야.
- 이전 질문들과 현재 질문들을 종합해서 질문을 분류해줘.

[이전 질문 목록]
---

## 출력 규칙
- **반드시** `'Taskn-n'` 형식으로만 출력 (설명, 부가 텍스트 금지)
- 다시 한 번 아래의 내용을 ! 반드시 확인해줘 !
**질문에 아래 중 하나라도 없다면 무조건 Task4로 분류한다.**
   - 날짜(예: "2024-07-01" 형식 또는 "2024년 7월 1일" 등 !구체적! 날짜 정보)
   - 종목명(예: "삼성전자", "현대차" 등 특정 기업명)
   - 명확한 기준 수치(예: "5% 이상", "2천만 주 이상" 등)
[출력 예시]
'삼성전자 가격이 어떻게 돼?' -> 언제 가격을 말하는지 모르므로 Task4
'안녕' -> 질문 자체가 모호하므로 Task4
'KOSDAQ에서 가장 비싼 종목 3개는?' -> 언제 기준 가장 비싼 종목인지 모르므로 Task4
'2025-04-16 종가는?' -> 어느 종목의 종가를 의미하는지 모호하므로 Task4

'''


task_4_prompt_clarifying = '''
[역할]
너는 데이터 분석가를 보조할 조교야. 
금융 데이터 분석 ai에 질문이 들어가기 전, 질문의 방향성을 명확히 하는 것이 너의 목표야.
너가 할 일은, 날짜, 거래량 기준, 비율, 종목과 같이 질문에 필수적인 요소의 부재를 파악하고, 이를 사용자에게 되묻는 프롬프트를 작성해주면 돼.

금융 데이터 분석 ai는 다음과 같은 질문들에 대해 답변할 수 있어.

[금융 데이터 분석 ai가 답변할 수 있는 질문 목록]
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

  


[너의 역할 예시]
예)
1.
원질문: '없음'
너의 응답: '무슨 말씀인지 잘 모르겠습니다. 금융 ai agent가 답변할 수 있도록 질문을 구체화해주세요.'
2.
원질문: '최근 많이 오른 주식 좀 알려줘'
너의 응답: '최근 많이 오른 주식의 의미를 조금 더 정확히 해 주세요!'
3. 
원질문: '고점 대비 많이 떨어진 주식을 알려줘'
너의 응답: '고점 대비 많이 떨어진 주식의 의미를 잘 모르겠습니다. 질문을 조금 더 구체화해 주실 수 있으신가요?'
4. 
원질문: '앞으로 뭘 사면 좋을까?'
너의 응답: '잘 모르겠습니다. 구체적 답변을 원하시면 조금 더 정보를 주세요!'

'''

error_check = '''
[역할]
너는 코드의 에러를 수정하는 ai야.
코드가 주어지면, 해당 python코드를 바로 로컬환경에서 실행할 수 있게 문법 오류를 수정해줘. 

[예시]
질문1:
```python
import pandas as pd

ticker_name = "도화엔지니어링"
target_date = "2025-06-25"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
high_data = stock_data[(stock_data['Price'] == 'High') & (stock_data['종목명'] == ticker_name)].copy()
high_only = high_data[date_cols].astype(float)

price = high_only[target_date].iloc[0]
print(f{price:,0f}원)
```
--> 이 코드는 \'\'\'와 같은 불필요한 ' 표시와, 불필요한 python 실행 명령어가 있어.
--> 또한, print(f{price:,0f}원)문법이 틀렸기 때문에, print(f"{price:,.0f}원")으로 바꿔줘야해

질문1에 대한 수정코드:
import pandas as pd

ticker_name = "도화엔지니어링"
target_date = "2025-06-25"

date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
high_data = stock_data[(stock_data['Price'] == 'High') & (stock_data['종목명'] == ticker_name)].copy()
high_only = high_data[date_cols].astype(float)

price = high_only[target_date].iloc[0]
print(f"{price:,.0f}원")

[마지막 확인]
- 절대 아무런 부연 설명을 덧붙이지 말고, 오로지 파이썬 코드만 내보내줘.
- 절대 ouput을 실행시키지 말고, 그냥 문법 오류만 고쳐서 완벽한 pure code만 제공해줘.
- 순수한 python코드만 제공해줘. 절대 부연설명을 붙이지마.
- output을 제공하라는 것이 아닌, 다시 순수한 python 코드를 제공하라는 것이야. 
- 내가 직접 실행 시킬 수 있는 문법 오류를 수정한 python 코드만 제공해줘. 

'''


final_common_prompt = '''
[역할]  
너는 주식 데이터를 다루는 데이터 분석가이자, [입력 질문]에 대한 **Python 코드**를 생성하는 AI야.  
**로컬에서 바로 실행할 수 있도록, 설명이나 텍스트 없이 오직 순수한 코드만 출력해야 해.**


[필수 검토 주의사항]
- 문자열 출력 시 다음 포맷을 준수해야 한다:
  - 정수형: `print(f"{price:,.0f}원")`  
  - 소수점 둘째 자리까지 필요할 때: `print(f"{price:,.2f}원")`
  - result의 type이 dataframe일 때, print(result)를 할 경우, text가 아닌 데이터프레임 자체로 output이 나가므로, 꼭 text를 ouput으로 내보낼 수 있도록 한다.
- 토요일·일요일(주말)에는 데이터가 없을 수 있다는 점을 고려해야 한다.
* 반드시 바로 실행시킬 수 있는 python 코드 '만'을 작성해줘. 절대 '코드:'으로 시작하는 등 python에서 실행시킬 수 없는 어떠한 요소도 넣지 마 **
- 바로 복사 붙여넣기 해서 실행시킬 수 있는 코드만 작성해.
* 계속 print(f"응답") 이거 쓰면서 따옴표 " 이거 빼먹는데, print(f 구문을 쓸 때는 항상 print(f"응답") 이렇게 "를 응답 주위에 감싸야 한다.
** 단일 종목을 답으로 내보내야할 경우, 필요한 숫자까지 뒤에 덧붙인다. 
** 가령, 거래량에 대해 물어봤을 때 거래량 정보를 뒤에 덧붙이거나, 종가에 대해 물어봤을 때, 종가에 대한 정보를 뒤에 덧붙이는 식으로.
예시) 질문:2024-09-12 KOSDAQ 시장에서 가장 비싼 종목은? 답: 알테오젠 (x) -> 알테오젠 (316,000원)
예시) 질문:2025-05-09 KOSDAQ 시장에서 거래량이 가장 많은 종목은? 답: 우리로 (x) -> 우리로 (37,729,480주)
*** 해당 날짜에 대한 데이터 접근이 안될 수 있음 (휴일 or 공휴일 등)
*** 따라서 항상 try 문을 통해 데이터가 없을 때는 오류가 아닌 데이터가 없다고 명시해야함
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


# "Task4-1": """
# 원질문: '{원질문}'
# 출력: "몇 월 며칠 기준으로 결과를 알고 싶으신가요?"
# """,

# "Task4-2": """
# 원질문: '{원질문}'
# 출력: "어떤 종목(회사명)을 말씀하시는 건가요?"
# """,

# "Task4-3": """
# 원질문: '{원질문}'
# 출력: "몇 퍼센트 이상(또는 몇 주 이상)으로 기준을 잡고 싶으신가요?"
# """,

# "Task4-4": """
# 원질문: '{원질문}'
# 출력: "어느 날짜 기준으로 어떤 종목(또는 조건)을 찾고 싶으신가요?"
# """,

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

try:
  date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
  open_data = stock_data[(stock_data['Price'] == 'Open') & (stock_data['종목명'] == ticker_name)].copy()
  open_only = open_data[date_cols].astype(float)

  price = open_only[target_date].iloc[0]
  print(f"{price:,.0f}원")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

2)
유형 : 단순조회_종가
질문 : {종목명}의 {날짜} 종가는?
답변 : {가격}원
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"
try:
  date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
  close_data = stock_data[(stock_data['Price'] == 'Close') & (stock_data['종목명'] == ticker_name)].copy()
  close_only = close_data[date_cols].astype(float)

  price = close_only[target_date].iloc[0]
  print(f"{price:,.0f}원")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

3)
유형 : 가격조회_등락률
질문 : {종목명}의 {날짜} 등락률은?
답변 : {등락률}%
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"

try:
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
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

4)
유형 : 가격조회_고가
질문 : {종목명}의 {날짜} 고가는?
답변 : {가격}원
코드 :
import pandas as pd

ticker_name = "{종목명}"
target_date = "{날짜}"
try:
  date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
  high_data = stock_data[(stock_data['Price'] == 'High') & (stock_data['종목명'] == ticker_name)].copy()
  high_only = high_data[date_cols].astype(float)

  price = high_only[target_date].iloc[0]
  print(f"{price:,.0f}원")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

''',

"Task1-2": '''
1)
유형 : 시장통계_상승종목수
질문 : {날짜}에 상승한 종목은 몇 개인가?
답변 : {개수}개
코드 :
import pandas as pd

target_date = "{날짜}"

try:
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
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

2)
유형 : 시장조회_KOSPI_market_count
질문 : {날짜} KOSPI 시장에 거래된 종목 수는?
답변 : {개수}개
코드 :
import pandas as pd

target_date = "{날짜}"

try:
  date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
  volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSPI')].copy()
  volume_only = volume_data[date_cols].astype(float)

  count = (volume_only[target_date] > 0).sum()
  print(f"{count}개")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

3)
유형 : 시장조회_KOSPI_top_volume
질문 : {날짜} KOSPI 시장에서 거래량이 가장 많은 종목은?
답변 : {종목명} ({거래량}주)
코드 :
import pandas as pd

target_date = "{날짜}"

try:
  date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
  volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSPI')].copy()
  volume_only = volume_data[date_cols].astype(float)

  volume_data['거래량'] = volume_data[target_date]
  top_row = volume_data.sort_values(by='거래량', ascending=False).iloc[0]
  print(f"{top_row['종목명']} ({int(top_row['거래량']):,}주)")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

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
  count = (close_data['현재종가'] > close_data['이전종가']).sum()

  print(f"{count}개")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

6)
유형 : 시장통계_거래대금
질문 : {날짜} 전체 시장 거래대금은?
답변 : {거래대금}원
코드 :
import pandas as pd

target_date = "{날짜}"

try:
  volume_data = stock_data[stock_data['Price'] == 'Volume'][['Ticker', target_date]].copy()
  volume_data = volume_data.rename(columns={target_date: 'Volume'})

  close_data = stock_data[stock_data['Price'] == 'Close'][['Ticker', target_date]].copy()
  close_data = close_data.rename(columns={target_date: 'Close'})

  final_data = pd.merge(volume_data, close_data, on='Ticker')

  final_data["거래대금"] = final_data["Volume"] * final_data["Close"]
  total_turnover = final_data["거래대금"].sum()

  print(f"{total_turnover:,.0f}원")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

7)
유형 : 시장조회_KOSDAQ_top_volume
질문 : {날짜} KOSDAQ 시장에서 거래량이 가장 많은 종목은?
답변 : {종목명} ({거래량}주)
코드 :
import pandas as pd

target_date = "{날짜}"

try:
  date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
  volume_data = stock_data[(stock_data['Price'] == 'Volume') & (stock_data['시장'] == 'KOSDAQ')].copy()
  volume_only = volume_data[date_cols].astype(float)

  volume_data['거래량'] = volume_data[target_date]
  top_row = volume_data.sort_values(by='거래량', ascending=False).iloc[0]
  print(f"{top_row['종목명']} ({int(top_row['거래량']):,}주)")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

8)
유형 : 시장통계_하락종목수
질문 : {날짜}에 하락한 종목은 몇 개인가?
답변 : {개수}개
코드 :
import pandas as pd

target_date = "{날짜}"

try:
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
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")
    
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

10)
유형 : 시장통계_지수비교_KOSPI_KOSDAQ
질문 : {날짜}에 KOSPI와 KOSDAQ 중 더 높은 지수는?
답변 : {시장명} ({지수값})
코드 :
import yfinance as yf
import pandas as pd

target_date = "{날짜}"

kospi = yf.Ticker("^KS11")
kosdaq = yf.Ticker("^KQ11")

# 최근 2년치 데이터 로드
kospi_df = kospi.history(period="2y")
kosdaq_df = kosdaq.history(period="2y")

try:
    kospi_value = kospi_df.loc[target_date]["Close"]
    kosdaq_value = kosdaq_df.loc[target_date]["Close"]

    if kospi_value > kosdaq_value:
        print(f"KOSPI ({kospi_value:.2f})")
    else:
        print(f"KOSDAQ ({kosdaq_value:.2f})")
except:
    print("해당 날짜에 존재하는 데이터가 없습니다.")

11)
유형 : 시장통계_개별종목_거래비중
질문 : {날짜}에 {종목명}의 거래량이 전체 시장 거래량의 몇 %인가?
답변 : {비중}% 또는 "해당 날짜 {종목명} 거래량 비중 데이터 없음"
코드:
import pandas as pd

target_date = "{날짜}"
target_stock = "{종목명}"

# 거래량 데이터 추출
volume_data = stock_data[stock_data['Price'] == 'Volume'].copy()

if target_date not in volume_data.columns:
    print(f"해당 날짜 {target_stock} 거래량 비중 데이터 없음")
else:
    volume_data = volume_data[['Ticker', '종목명', target_date]].copy()
    volume_data = volume_data.rename(columns={target_date: '거래량'})

    total_volume = volume_data['거래량'].sum()

    target_row = volume_data[volume_data['종목명'] == target_stock]

    if not target_row.empty and total_volume > 0:
        target_volume = target_row['거래량'].values[0]
        ratio = (target_volume / total_volume) * 100
        print(f"{ratio:.2f}%")
    else:
        print(f"해당 날짜 {target_stock} 거래량 비중 데이터 없음")
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

'Task1-4': '''
1) 
유형 : 종목비교_종가비교
질문 : {날짜}에 {종목1}과 {종목2} 중 종가가 더 높은 종목은?
답변 : {종목명} ({종가}원) 또는 "해당 날짜에 종가 비교 데이터 없음"
코드:
import pandas as pd

target_date = "{날짜}"
stock1 = "{종목1}"
stock2 = "{종목2}"

close_data = stock_data[stock_data['Price'] == 'Close'].copy()

# 날짜 유효성 확인
if target_date not in close_data.columns:
    print("해당 날짜에 종가 비교 데이터 없음")
else:
    # 두 종목의 데이터 필터링
    close_data = close_data[['종목명', 'Ticker', target_date]]
    filtered = close_data[close_data['종목명'].isin([stock1, stock2])]

    if filtered.shape[0] < 2:
        print("해당 날짜에 종가 비교 데이터 없음")
    else:
        filtered = filtered.rename(columns={target_date: '종가'})
        top_row = filtered.sort_values(by='종가', ascending=False).iloc[0]
        print(f"{top_row['종목명']} ({int(top_row['종가']):,}원)")

        
2)
유형: 종목비교_시장평균_등락률비교
질문: {날짜}에 {종목명}의 등락률이 시장 평균보다 높은가?
답변: 예 / 아니오 / 데이터 없음
코드:
import pandas as pd

target_date = "{날짜}"
target_stock = "{종목명}"

# 종가 데이터 필터링
close_data = stock_data[stock_data['Price'] == 'Close'].copy()
date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data[date_cols] = close_data[date_cols].astype(float)

# 이전 날짜 계산
prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')
if target_date not in close_data.columns or prev_date not in close_data.columns:
    print("데이터 없음")
else:
    # 전체 등락률 평균 계산
    close_data['등락률'] = (close_data[target_date] - close_data[prev_date]) / close_data[prev_date] * 100
    market_avg = close_data['등락률'].mean()

    # 대상 종목 등락률 추출
    target_row = close_data[close_data['종목명'] == target_stock]
    if target_row.empty:
        print("데이터 없음")
    else:
        target_return = target_row['등락률'].values[0]
        if target_return > market_avg:
            print("예")
        else:
            print("아니오")

3)
유형: 종목비교_등락률비교
질문: {날짜}에 {종목1}과 {종목2} 중 등락률이 더 높은 종목은?
답변: {종목명} ({등락률}%) 또는 데이터 없음
코드:

import pandas as pd

target_date = "{날짜}"
stock1 = "{종목1}"
stock2 = "{종목2}"

close_data = stock_data[stock_data['Price'] == 'Close'].copy()
date_cols = [c for c in stock_data.columns if c not in ['Price','Ticker','시장','종목명']]
close_data[date_cols] = close_data[date_cols].astype(float)

# 이전 날짜 계산
prev_date = pd.to_datetime(target_date) - pd.Timedelta(days=1)
prev_date = prev_date.strftime('%Y-%m-%d')

if target_date not in close_data.columns or prev_date not in close_data.columns:
    print("데이터 없음")
else:
    # 종목 필터링 및 등락률 계산
    subset = close_data[close_data['종목명'].isin([stock1, stock2])].copy()
    if subset.shape[0] < 2:
        print("데이터 없음")
    else:
        subset['등락률'] = (subset[target_date] - subset[prev_date]) / subset[prev_date] * 100
        top_row = subset.sort_values(by='등락률', ascending=False).iloc[0]
        print(f"{top_row['종목명']} ({top_row['등락률']:.2f}%)")
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
print(", ".join(result))

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
print(", ".join(result))
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
print(", ".join(result))

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
print(", ".join(result))
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
print(", ".join(result))

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
print(", ".join(result))
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
print(", ".join(result))

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
print(", ".join(result))
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
print(", ".join(result))

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
print(", ".join(result))

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
print(", ".join(result))

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
print(", ".join(result))
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
print(", ".join(result))

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
print(", ".join(result))
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
print(", ".join(result))

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
print(", ".join(result))
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

print(", ".join(result))

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

print(", ".join(result))
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



last_warning_prompt = '''
[답하기 전 마지막 꼭 지켜야 할 당부의 말]
- 절대 '코드:'으로 시작하는 등 python에서 실행시킬 수 없는 어떠한 요소도 넣지 마.
- 바로 복사 붙여넣기 해서 실행시킬 수 있는 코드만 작성해.
- 너 진짜 계속 print(f"응답") 이거 쓰면서 따옴표 " 이거 빼먹는데, f 구문을 쓸 때는 항상 print(f"응답") 이렇게 "를 응답 주위에 감싸야 한다.
** 제발 마지막으로 확인해. print(f"")에 따옴표 잘 붙혔는지. 이거 빼먹으면 절대!!!!! 절대!!!! 안된다.
예시) print(f{종목명}) -> print(f"{종목명}")
- print(f"{price:,0f}원")과 같은 문법 오류도 있는지 확인하고 고쳐.
예시) print(f"{price:,0f}원") ->  print(f"{price:,.0f}원")
'''