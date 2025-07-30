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


# input 들만 id 별로 저장 (task 종류, 질문)
request_uuids = {
    'example id': [['Task4-1','안녕하세요?'],['Task4-1','kospi 시장에서 상승 종목 수']['Task1-1','2024년 1월 18일에 KOSPI 시장에서 상승한 종목 수는? ']]
}

@app.get("/")
async def get_answer(
    question: str = Query(..., description="질문 내용"),
    authorization: str = Header(..., alias="Authorization"),
    request_id: str = Header(..., alias="X-NCP-CLOVASTUDIO-REQUEST-ID")
):
    logger.info(f'question: {question}')

    try:
        # 1차 분류 (Task1~4 구분)
        
        classification_answer = call_clova.call_clova_find_intention(
            question,
            api_key=authorization,
            request_id=request_id
        )
        logger.info(f'task classification: {classification_answer}')
        ##저장
        if request_id in request_uuids:
            request_uuids[request_id].append([f"{classification_answer}",question])
            

        # --- Task4 (모호 질문) 처리 --- (모호하면 다시 질문 시킴.)
        if classification_answer.startswith("Task4"):
            logger.info('this is task4 question')
            pardon_answer = call_clova.call_clova_task4(
                question,
                api_key=authorization,
                request_id=request_id
            )
            logger.info(f'Task4 clarification output: {pardon_answer}')
            return JSONResponse(
                content={"type": "clarification", "message": pardon_answer},
                status_code=200
            )
            

        # --- Task1~3 (정확 질문 → 코드 생성 & 실행) --- 마지막 실행!
        
        answer = call_clova.call_clova(
            question,
            api_key=authorization,
            request_id=request_id,
            pre_prompt_map=classification_answer
        )
        answer = answer.strip()
        logger.info(f'raw answer: {answer}')

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        exec(answer, globals())
        final_answer = mystdout.getvalue().strip()
        return JSONResponse(
                content={"type": "final answer", "message": final_answer},
                status_code=200
            )
    
    except Exception as e:
        logger.info(f'error: {e}')
        return JSONResponse(
                content={"type": "error", "message": str(e)},
                status_code=200
            )
            



    #     # 코드 실행 처리
    #     output = ''
    #     if isinstance(answer, str):
    #         cleaned = answer.strip()
    #         if cleaned.startswith("```"):
    #             cleaned = "\n".join(
    #                 line for line in cleaned.splitlines() 
    #                 if not line.strip().startswith("```")
    #             )
    #         logger.info(f'cleaned code: {cleaned}')

    #         try:
    #             old_stdout = sys.stdout
    #             sys.stdout = mystdout = StringIO()
    #             exec(cleaned, globals())
    #             output = mystdout.getvalue().strip()
    #             return output
    #         except Exception as e:
    #             print(f'error: {e}')
    # except Exception as e:
    #     print(f'error: {e}')