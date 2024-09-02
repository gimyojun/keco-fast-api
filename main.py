# main.py
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
import json

from models import Message, CardUpdateRequest  # models.py에서 임포트

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/r2/code/list")
async def code_list(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = Message(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    with open('data.json', 'r', encoding='utf-8') as f:
        response_content = json.load(f)

    return JSONResponse(content=response_content)

@app.post("/r2/card/update")
async def update_card(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = CardUpdateRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    response_data = {
        "result": "0",
        "rdate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "reqcnt": len(request_data.card),
        "inscnt": 0,
        "updcnt": len(request_data.card),
        "dupcnt": 0,
        "limitcnt": 0,
        "errcnt": 0,
        "errlist": []
    }
    logger.info(f"Response data: {response_data}")

    return JSONResponse(content=response_data)