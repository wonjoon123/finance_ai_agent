# AI Stock Data QA System

## 1. 프로젝트 개요
이 프로젝트는 주식 데이터를 대상으로 자연어 질의를 받아 **실행 가능한 Python 코드**로 변환하고, 그 결과를 사용자에게 반환하는 AI 기반 질의응답 시스템입니다.  
질문이 모호할 경우, 하나의 request id에 대해 AI가 자동으로 재질문(clarifying question)을 하여 추가 정보를 받아 2~5턴의 멀티턴 대화를 처리할 수 있습니다.

### 핵심 기능
1. 자연어 질문(Task1~Task4) 자동 분류
2. 모호 질문(Task4) → 재질문 및 멀티턴 처리
3. 명확한 질문(Task1~Task3) → 실행 가능한 Python 코드 자동 생성
4. 코드 실행 결과 반환

---

## 2. 시스템 아키텍처

### 구성 요소
#### 1) requesting.py (사용자 → 서버)
- 역할: 사용자 입력을 받아 FastAPI 서버(`main.py`)로 전달하는 클라이언트 스크립트
- 동작:
  - 사용자에게 질문을 입력받음 (`input()`)
  - GET 요청으로 질문과 인증 헤더를 서버로 전송
  - 서버로부터 받은 결과(`answer`)를 콘솔에 출력

#### 2) main.py (FastAPI 서버)
- 역할: 전체 질문→답변 파이프라인 중심
- 동작:
  - SQLite 데이터베이스(`finance.db`)에서 `stock_list`, `stock_data` 로드
  - `/` 엔드포인트에서 질문 수신
  - `call_clova_find_intention()`으로 Task 분류
  - Task4 → `call_clova_task4()`로 재질문 반환
  - Task1~3 → `call_clova()`로 코드 생성 후 `exec()` 실행 및 결과 반환

#### 3) call_clova.py (Clova API 호출 모듈)
- 역할: Clova Studio LLM API 호출
- 동작:
  - `call_clova_find_intention()` → 질문 의도(Task1~4) 분류
  - `call_clova_task4()` → 모호 질문 시 재질문 생성
  - `call_clova()` → Task1~3 질문에 대한 실행 가능한 Python 코드 생성
- 특징:
  - `pre_prompt.py`에 정의된 프롬프트(find_intention, task_4_prompt_clarifying, final_common_prompt 등) 기반

#### 4) pre_prompt.py (LLM 프롬프트 저장소)
- 역할: Clova LLM이 사용할 프롬프트 템플릿 관리
- 동작:
  - `find_intention`: 질문을 Task로 분류하는 규칙
  - `task_4_prompt_clarifying`: 모호 질문 시 재질문
  - `final_common_prompt` + `prompt_map`: Task1~3 질문 → Python 코드 템플릿 제공
  - `last_warning_prompt`: 코드 출력 시 규칙

### 전체 동작 흐름
사용자 입력
↓ (requesting.py)
FastAPI 서버(main.py)
↓
질문 분류 (call_clova_find_intention, pre_prompt.find_intention)
↓
┌─ Task4 (모호) → call_clova_task4 → 재질문 → 사용자 응답 → 재분류
└─ Task1~3 (명확) → call_clova → 실행 가능한 코드 생성 → exec() 실행
↓
실행 결과 반환

---

## 3. API 사용법

### Base URL
base_url = 'http://49.50.129.227:8000/'  

### 엔드포인트
#### `GET /`
- **설명:** 사용자 질문에 대한 답변을 반환합니다.
- **Query Parameters:**
  - `question` (string, 필수) – 사용자 입력 질문
- **Headers:**
  - `Authorization` – 하이퍼클로바 LLM API 키 (예: `Bearer <YOUR-CLOVA-API-KEY>`)
  - `X-NCP-CLOVASTUDIO-REQUEST-ID` – 요청 고유 ID (UUID 권장) (선택, 기본값 None) (task 5의 멀티턴에 대해서만 사용됨.)
- **Response:**
```json
{
  "answer": "질의 결과 또는 재질문",
  "request_id": id (멀티턴 시 입력값에 사용됨)
}
### 예시 요청 (Example Request)
bash
curl -G "http://49.50.129.227:8000/" \
  --data-urlencode "question=2024-07-18에 등락률이 +5% 이상인 종목을 모두 보여줘" \
  -H "Authorization: Bearer <YOUR-CLOVA-API-KEY>" \
  -H "X-NCP-CLOVASTUDIO-REQUEST-ID: 1234"

python
url = "http://49.50.129.227:8000/"
params = {
    "question": question
}
headers = {
    "Authorization": "Bearer <YOUR-CLOVA-API-KEY>"  # 실제 API 키 입력
    // ,"X-NCP-CLOVASTUDIO-REQUEST-ID": '1'  멀티턴의 경우 request_id 추가
}
response = requests.get(url, params=params, headers=headers)

### 예시 응답 (Example Response)
json
{
  "answer": "DXVX, 엑스큐어, 샤페...",
  "request_id": '2'
}


## task5: 멀티턴
- 멀티턴을 요하는 질문의 경우 request_id를 input에 추가함으로써 대화를 이어나갈 수 있음.

예시) (request_id 별로 다른 멀티턴 대화를 이어갈 수 있음.)
Q: 하이
A: 안녕하세요! 금융 데이터 분석 인공지능을 보조할 조교입니다. 
궁금하신 내용이나 요청하실 사항이 있으면 언제든지 말씀해주세요. 제가 최대한 도움을 드리겠습니다.
Q: 삼성전자 종가 알려주라
A: 어느 날짜의 삼성전자 종가를 알고 싶으신가요? 날짜를 말씀해 주신다면 해당 날짜의 삼성전자 종가를 알려드리겠습니다.
Q: 2024년 11월 11일의 종가
A: 54,305원

사용 방법:
1. 일단 request_id를 추가하지 않고 답변을 받는다.
2. 답변을 받고, 멀티턴으로 요청하고 싶은 대화의 경우 받은 request_id를 입력값에 넣는다.
3. 멀티턴을 이어간다.

주의사항:
-멀티턴의 경우 대화당 총 10회로 제한되어 있습니다.


- 더 자세한 requesting 방법은 requesting.py를 참고하시오.