import requests
import uuid
import pre_prompt
from logger_config import setup_logger

logger = setup_logger("call_clova")
logger.info("Starting call_clova!")

API_URL = "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003"

# ---- Task4 멀티턴 상태 저장 ----
task4_sessions = {}  # {request_id: {"original_question": str, "task4_type": str}}

def call_clova(user_input, api_key, request_id, pre_prompt_map: str):
    messages = [
        {
            "role": "system",
            "content": pre_prompt.final_common_prompt + '\n' + pre_prompt.prompt_map[pre_prompt_map]
        },
        {"role": "user", "content": user_input}
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key,
        "X-NCP-CLOVASTUDIO-REQUEST-ID": request_id
    }

    payload = {
        "messages": messages,
        "topP": 0.8,
        "topK": 0,
        "temperature": 0.7,
        "maxTokens": 4096,
        "repeatPenalty": 5.0,
        "stopBefore": [],
        "includeTokens": False
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()["result"]["message"]["content"]
        logger.info(f'final_result: {result}')
        return result
    else:
        logger.error(f"❌ Error: {response.status_code} {response.text}")
        return "call_clova에서 오류가 발생했습니다."


def call_clova_1(user_input, api_key, request_id):
    # ---- Task4 보강 질문 처리 ----
    if request_id in task4_sessions:
        session = task4_sessions.pop(request_id)
        combined_question = f"{session['original_question']}\n{user_input}"
        logger.info(f"Task4 follow-up → combined question: {combined_question}")

        # Task 재분류 (Task1~3) 후 반환
        return _classify_and_return(combined_question, api_key, request_id)

    # ---- 최초 Task 분류 ----
    return _classify_and_return(user_input, api_key, request_id)


def _classify_and_return(user_input, api_key, request_id):
    messages = [
        {"role": "system", "content": pre_prompt.find_intention},
        {"role": "user", "content": user_input}
    ]
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key,
        "X-NCP-CLOVASTUDIO-REQUEST-ID": request_id
    }
    payload = {
        "messages": messages,
        "topP": 0.8,
        "topK": 0,
        "temperature": 0.7,
        "maxTokens": 1024,
        "repeatPenalty": 5.0,
        "stopBefore": [],
        "includeTokens": False
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()["result"]["message"]["content"]
        logger.info(f'first_result: {result}')

        # ---- Task4 감지 시 세션 저장 ----
        if result.startswith("Task4"):
            task4_sessions[request_id] = {"original_question": user_input, "task4_type": result}
            # Task4 응답 리턴
            return pre_prompt.prompt_map.get(result, "추가 정보가 필요합니다. 조건을 더 입력해 주세요.")

        return result
    else:
        logger.error(f"❌ Error: {response.status_code} {response.text}")
        return "call_clova에서 오류가 발생했습니다."
