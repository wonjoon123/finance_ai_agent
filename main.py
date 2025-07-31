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
    'example id': [['Task4-1','안녕하세요?'],['Task4-1','kospi 시장에서 상승 종목 수'],['Task1-1','2024년 1월 18일에 KOSPI 시장에서 상승한 종목 수는? ']]
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

        ### 이전 대화내용 복구
        if request_id in request_uuids:
            session_history = request_uuids[request_id]
            if len(session_history) >= 5:   # 5턴 제한
                return JSONResponse(content={"answer": "대화가 너무 길어졌습니다. 다시 질문해주세요."})
            # 과거 대화 + 현재 질문 합치기
            prev_questions = []
            ambiguous_questions = []

            for s in session_history:
                if s['task'].startswith('Task4'):
                    ambiguous_questions.append(s['question'])
                else:
                    prev_questions.append(s['question'])

            # 텍스트 조립
            prev_texts = '[이전질문]\n' + "\n".join(prev_questions) if prev_questions else ''
            ambiguous_part = "\n".join(ambiguous_questions)

            # 최종 현재 질문
            if ambiguous_part:
                full_question = f"{ambiguous_part}\n{question}"
            else:
                full_question = question

            # 전체 input 구성
            added_question = f"{prev_texts}\n[현재질문]{full_question}" if prev_texts else f"[현재질문]{full_question}"
        else:
            added_question = question

        logger.info(added_question)
        
        classification_answer = call_clova.call_clova_find_intention(
            added_question,
            api_key=authorization,
            request_id=request_id
        )
        logger.info(f'task classification: {classification_answer}')
        ##저장
        if request_id in request_uuids:
            request_uuids[request_id].append({"task": classification_answer, "question": question})
        else:
            request_uuids[request_id] = [{"task": classification_answer, "question": question}]

        #logger
        logger.info(request_uuids)
            

        # --- Task4 (모호 질문) 처리 --- (모호하면 다시 질문 시킴.)
        if classification_answer.startswith("Task4"):
            logger.info('this is task4 question')
            pardon_answer = call_clova.call_clova_task4(
                question,
                api_key=authorization,
                request_id=request_id
            )
            logger.info(f'Task4 clarification output: {pardon_answer}')
            return JSONResponse(content={
            "answer": pardon_answer
            })
            

        # --- Task1~3 (정확 질문 → 코드 생성 & 실행) --- 마지막 실행!
        # 코드 생성!
        answer = call_clova.call_clova(
            question,
            api_key=authorization,
            request_id=request_id,
            pre_prompt_map=classification_answer
        )
        answer = answer.strip()
        logger.info(f'raw answer: {answer}')


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
        logger.info(f'\n\ncleaned code: {cleaned}')
        
            # stdout을 StringIO로 바꿔서 exec 결과 캡처
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        exec(cleaned, globals())  # 필요 시 locals()도 가능

        output = mystdout.getvalue().strip()
        

        logger.info(output)
        return JSONResponse(content={
            "answer": output
        })
    except Exception as e:
        return JSONResponse(content={
            "answer": f'main error: {str(e)}'
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