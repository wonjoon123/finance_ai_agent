import requests
import uuid
import pre_prompt
from logger_config import setup_logger
import config

logger = setup_logger("call_clova")
logger.info("Starting call_clova!")

API_URL = "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003"


# 질문이 모호할 때 재질문 보내기
def call_clova_task4(user_input, api_key, request_id):
    messages = [
        {"role": "system", "content": pre_prompt.task_4_prompt_clarifying},
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


        return result
    else:
        logger.error(f"call clova task4 Error: {response.status_code} {response.text}")
        return "call_clova에서 오류가 발생했습니다."



## help me find the intention in the question clova!
def call_clova_find_intention(user_input, api_key, request_id):
    
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
        return result
    else:
        logger.error(f"call clova Error intention: {response.status_code} {response.text}")
        return "call_clova에서 오류가 발생했습니다."


### 유저 인풋이 들어왔을 때, 
# def _classify_and_return(user_input, api_key, request_id):
#     messages = [
#         {"role": "system", "content": pre_prompt.find_intention},
#         {"role": "user", "content": user_input}
#     ]
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": api_key,
#         "X-NCP-CLOVASTUDIO-REQUEST-ID": request_id
#     }
#     payload = {
#         "messages": messages,
#         "topP": 0.8,
#         "topK": 0,
#         "temperature": 0.7,
#         "maxTokens": 1024,
#         "repeatPenalty": 5.0,
#         "stopBefore": [],
#         "includeTokens": False
#     }

#     response = requests.post(API_URL, headers=headers, json=payload)
#     if response.status_code == 200:
#         result = response.json()["result"]["message"]["content"]

#         # ---- Task4 감지 시 세션 저장 ----
#         if result.startswith("Task4"):
#             task4_sessions[request_id] = {"original_question": user_input, "task4_type": result}
#             # Task4 응답 리턴
#             return pre_prompt.prompt_map.get(result, "추가 정보가 필요합니다. 조건을 더 입력해 주세요.")

#         return result
#     else:
#         logger.error(f"❌ Error: {response.status_code} {response.text}")
#         return "call_clova에서 오류가 발생했습니다."


# 마지막 1,2,3 분류 되고 실행파일 만들기 도와줘 클로바
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
        # logger.info(f'final_result: {result}')
        return result
    else:
        logger.error(f"call clova final Error: {response.status_code} {response.text}")
        return "call_clova에서 오류가 발생했습니다."