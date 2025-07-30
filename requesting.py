import requests
import uuid

# 1. API URL
url = "http://49.50.129.227:8000/"

# 2. 사용자로부터 질문 입력 받기
question = input("질문을 입력하세요: ")

# 3. 쿼리 파라미터
params = {
    "question": question
}

# 4. 헤더 정보
headers = {
    "Authorization": "Bearer nv-bf23d32f4c3e41dea18865abcc2f2e4f75WU",  # 실제 API 키 입력
    "X-NCP-CLOVASTUDIO-REQUEST-ID": '1'
}

# 5. GET 요청 보내기
response = requests.get(url, params=params, headers=headers)

# 6. 결과 출력
if response.status_code == 200:
    print("✅ 응답:", response.json()['answer'])
else:
    print("❌ 에러 발생:", response.status_code)
    print(response.text)
