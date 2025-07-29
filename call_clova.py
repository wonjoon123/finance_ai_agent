import requests
import uuid

import json

import pre_prompt

from logger_config import setup_logger

logger = setup_logger("call_clova")
logger.info("Starting call_clova!")

API_URL = "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003"

# 코드 산출 클로바
def call_clova(user_input,api_key,request_id,pre_prompt_map:str):
    # 초기 시스템 역할 설정
    messages = [
        {
            "role": "system",
            "content": pre_prompt.final_common_prompt_01 + '\n' + pre_prompt.prompt_map[pre_prompt_map] + '\n' + pre_prompt.final_common_prompt_02 ## 여기서 메인으로 pre_prompt가 들어감.
        }
    ]
    messages.append({"role": "user", "content": user_input})
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{api_key}",
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
        messages.append({"role": "assistant", "content": result})
        logger.info(f'final_result: {result}')
        return result
    else:
        print(f"❌ Error: {response.status_code}")
        logger.info(f"❌ Error: {response.status_code}")
        logger.info(response.text)
        print(response.text)
        return "call_clova에서 오류가 발생했습니다."
    


# 질문 종류 판단 클로바
def call_clova_1(user_input,api_key,request_id):
    # 초기 시스템 역할 설정
    messages = [
        {
            "role": "system",
            "content": pre_prompt.find_intention ## 여기서 메인으로 pre_prompt가 들어감.
        }
    ]
    messages.append({"role": "user", "content": user_input})
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{api_key}",
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
        messages.append({"role": "assistant", "content": result})
        logger.info(f'first_result: {result}')
        return result
    else:
        print(f"❌ Error: {response.status_code}")
        logger.info(f"❌ Error: {response.status_code}")
        logger.info(response.text)
        print(response.text)
        return "call_clova에서 오류가 발생했습니다."

if __name__ == "__main__":
    print("💬 Clova Studio ChatBot (종료하려면 'exit')")
    while True:
        user_input = input("👤 당신: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 종료합니다.")
            break

        answer = call_clova_1(user_input,"Bearer nv-bf23d32f4c3e41dea18865abcc2f2e4f75WU",str(uuid.uuid4()))
        print(f"🤖 챗봇: {answer}\n")
