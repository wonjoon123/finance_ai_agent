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

# DB 연결
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

    try:
        # 1차 분류 (Task1~4 구분)
        first_answer = call_clova.call_clova_1(
            question,
            api_key=authorization,
            request_id=request_id
        )
        logger.info(f'first_result: {first_answer}')

        # --- Task4 (모호 질문) 처리 ---
        if first_answer.startswith("Task4"):
            output = call_clova.call_clova(
                question,
                api_key=authorization,
                request_id=request_id,
                pre_prompt_map=first_answer
            )
            logger.info(f'Task4 clarification output: {output}')
            return JSONResponse(
                content={"type": "clarification", "message": output},
                status_code=200
            )

        # --- Task1~3 (정확 질문 → 코드 생성 & 실행) ---
        answer = call_clova.call_clova(
            question,
            api_key=authorization,
            request_id=request_id,
            pre_prompt_map=first_answer
        )
        logger.info(f'raw answer: {answer}')

        # 코드 실행 처리
        output = ''
        if isinstance(answer, str):
            cleaned = answer.strip()
            if cleaned.startswith("```"):
                cleaned = "\n".join(
                    line for line in cleaned.splitlines() 
                    if not line.strip().startswith("```")
                )
            logger.info(f'cleaned code: {cleaned}')

            try:
                old_stdout = sys.stdout
                sys.stdout = mystdout = StringIO()
                exec(cleaned, globals())
                output = mystdout.getvalue().strip()
            except Exception as e:
