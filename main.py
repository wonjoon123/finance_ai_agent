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


a = 0
# input 들만 id 별로 저장 (task 종류, 질문)
request_uuids = {
    'example id': ['안녕하세요?','무슨 말씀이신지 모르겠습니다.']
}

@app.get("/")
async def get_answer(
    question: str = Query(..., description="질문 내용"),
    authorization: str = Header(..., alias="Authorization"),
    request_id: str = Header(None, alias="X-NCP-CLOVASTUDIO-REQUEST-ID")
):
    global a
    logger.info(f'question: {question}')

    try:
        # 1차 분류 (Task1~4 구분)
        a = a+1
        ### 이전 대화내용 복구
        if request_id is not None:
            
            session_history = request_uuids[request_id]
            if len(session_history) >= 10:   # 10턴 제한
                return JSONResponse(content={"answer": "대화가 너무 길어졌습니다. 다시 질문해주세요.",'request_id': request_id})

            # 모든 이전 질문 + 답변 합치기
            prev_texts = "[이전질문답변]\n" + "\n".join([f"{s}" for s in session_history])

            # 현재 질문 붙이기
            added_question = f"{prev_texts}\n[현재질문]{question}"
        else:
            added_question = f"[현재질문]{question}"
        
        classification_answer = call_clova.call_clova_find_intention(
            added_question,
            api_key=authorization,
            request_id=request_id
        )
        logger.info(f'task classification: {classification_answer}')
        ##저장

        if request_id is not None:
            request_uuids[request_id].append(question)
        else:
            request_uuids[str(a)] = [question]
           

        #logger

            

        # --- Task4 (모호 질문) 처리 --- (모호하면 다시 질문 시킴.)
        if classification_answer.startswith("Task4"):
            logger.info('this is task4 question')
            pardon_answer = call_clova.call_clova_task4(
                question,
                api_key=authorization,
                request_id=request_id
            )
            logger.info(f'Task4 clarification output: {pardon_answer}')
            if request_id is not None:
                request_uuids[request_id].append(pardon_answer)
                return JSONResponse(content={
                "answer": pardon_answer,
                'request_id': request_id
                })
            else:
                request_uuids[str(a)].append(pardon_answer)
                return JSONResponse(content={
                "answer": pardon_answer,
                'request_id': str(a)
                })
 

        # --- Task1~3 (정확 질문 → 코드 생성 & 실행) --- 마지막 실행!
        # 코드 생성!
        answer = call_clova.call_clova(
            added_question,
            api_key=authorization,
            request_id=request_id,
            pre_prompt_map=classification_answer
        )

        answer = answer.strip()


        # 코드 한 번 더 체크해서 final 실행!
        # answer = call_clova.call_clova(
        #     pre_answer,
        #     api_key=authorization,
        #     request_id=request_id,
        #     pre_prompt_map=classification_answer
        # )
        # logger.info(f'final code: {answer}')
        
        # 너무 말 안들어서 일단 제거
        
        cleaned = answer.strip()
        if cleaned.startswith("```"):
            cleaned = "\n".join(line for line in cleaned.splitlines() if not line.strip().startswith("```"))

        
            # stdout을 StringIO로 바꿔서 exec 결과 캡처
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        exec(cleaned, globals())  # 필요 시 locals()도 가능

        output = mystdout.getvalue().strip()
        

        logger.info(output)
        
        return JSONResponse(content={
            "answer": output,
            'request_id': str(a)
        })
    except Exception as e:
        return JSONResponse(content={
            "answer": f'잘 모르겠습니다 (에러상황: {str(e)})',
            'request_id': str(a)
        })

    #     old_stdout = sys.stdout
    #     sys.stdout = mystdout = StringIO()
    #     exec(answer, globals())
    #     final_answer = mystdout.getvalue().strip()
    #     return JSONResponse(
    #             content={"type": "final answer", "message": final_answer},
    #             status_code=200
    #         )
    
    # except Exception as e:
    #     logger.info(f'error: {e}')
    #     return JSONResponse(
    #             content={"type": "error", "message": str(e)},
    #             status_code=200
    #         )
            



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