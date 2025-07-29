from fastapi import FastAPI, Header, Query
from fastapi.responses import JSONResponse
import call_clova
import pre_prompt
import pandas as pd
import sqlite3
from io import StringIO
import sys
from logger_config import setup_logger


logger = setup_logger("main")

logger.info("Starting app...")


app = FastAPI()

conn = sqlite3.connect('finance.db')
stock_list = pd.read_sql_query("SELECT * FROM stock_list;", conn)
stock_data = pd.read_sql_query("SELECT * FROM stock_data;", conn)
conn.close()



@app.get("/")
async def get_answer(
    question: str = Query(..., description="질문 내용"),
    authorization: str = Header(..., alias="Authorization"),
    request_id: str = Header(..., alias="X-NCP-CLOVASTUDIO-REQUEST-ID")
):

    logger.info(f'question: {question}')
    logger.debug(f'authorization: {authorization}')
    # 여기서 자연어 질문에 대해 실제 처리를 수행

    # 질문 구분
    first_answer = call_clova.call_clova_1(question,api_key=authorization,request_id=request_id)
    logger.info(f'\n\nfirst answer: {first_answer}')

    # 최종 결과 코드
    answer = call_clova.call_clova(question,api_key=authorization,request_id=request_id,pre_prompt_map = first_answer)
    logger.info(f'\n\nraw answer: {answer}')

    output = ''

    # 최종 결과 코드 실행
    if isinstance(answer, str):
        cleaned = answer.strip()
        if cleaned.startswith("```"):
            cleaned = "\n".join(line for line in cleaned.splitlines() if not line.strip().startswith("```"))
        logger.info(f'\n\ncleaned code: {cleaned}')
        try:
            # stdout을 StringIO로 바꿔서 exec 결과 캡처
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

            exec(cleaned, globals())  # 필요 시 locals()도 가능

            output = mystdout.getvalue().strip()
        except Exception as e:
            output = f"❌ main 코드 실행 중 오류: {e}"
        finally:
            sys.stdout = old_stdout
    else:
        output = "❌ answer는 문자열이 아닙니다."

    logger.info(output)
    return JSONResponse(content={
        "answer": output
    })

# @app.get("/")
# async def get_answer(
#     question: str = Query(..., description="질문 내용"),
#     authorization: str = Header(..., alias="Authorization"),
#     request_id: str = Header(..., alias="X-NCP-CLOVASTUDIO-REQUEST-ID")
# ):

#     logger.info(f'question: {question}')
#     logger.debug(f'authorization: {authorization}')
#     # 여기서 자연어 질문에 대해 실제 처리를 수행
#     # full_promt = f"{pre_2}{question}"

#     answer = call_clova.call_clova_1(question,api_key=authorization,request_id=request_id)
#     logger.info(f'\n\nraw answer: {answer}')

#     output = ''

#     if isinstance(answer, str):
#         cleaned = answer.strip()
#         if cleaned.startswith("```"):
#             cleaned = "\n".join(line for line in cleaned.splitlines() if not line.strip().startswith("```"))
#         logger.info(f'\n\ncleaned code: {cleaned}')
#         try:
#             # stdout을 StringIO로 바꿔서 exec 결과 캡처
#             old_stdout = sys.stdout
#             sys.stdout = mystdout = StringIO()

#             exec(cleaned, globals())  # 필요 시 locals()도 가능

#             output = mystdout.getvalue().strip()
#         except Exception as e:
#             output = f"❌ main 코드 실행 중 오류: {e}"
#         finally:
#             sys.stdout = old_stdout
#     else:
#         output = "❌ answer는 문자열이 아닙니다."

#     logger.info(output)
#     return JSONResponse(content={
#         "answer": output
#     })