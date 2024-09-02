from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import List
import json
from datetime import datetime
import logging

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 공통코드 요청 관련 모델
class Message(BaseModel):
    bid: str
    bkey: str

    @validator('bid')
    def validate_bid(cls, v):
        if len(v) != 2 or v not in ['EV', 'KP']:
            raise ValueError('bid는 "EV" 또는 "KP"이어야 합니다.')
        return v

    @validator('bkey')
    def validate_bkey(cls, v):
        if len(v) != 16:
            raise ValueError('bkey는 16자리여야 합니다.')
        return v

@app.post("/r2/code/list")
async def code_list(messages: str = Form(...)):
    try:
        # messages 필드의 JSON 데이터를 파싱하여 Pydantic 모델로 변환
        parsed_data = json.loads(messages)
        request_data = Message(**parsed_data)

        # 요청받은 데이터를 로깅
        logger.info(f"Received request data: {request_data}")

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    # 데이터 파일 읽기
    with open('data.json', 'r', encoding='utf-8') as f:
        response_content = json.load(f)

    return JSONResponse(content=response_content)

# 새로운 CardUpdate 관련 모델
class CardUpdate(BaseModel):
    no: str
    stop: str

    @validator('no')
    def validate_no(cls, v):
        if len(v) != 16 or not v.isdigit():
            raise ValueError('회원카드는 16자리 숫자형식입니다.')
        return v

    @validator('stop')
    def validate_stop(cls, v):
        if v not in ('Y', 'N'):
            raise ValueError('stop 필드는 Y 또는 N이어야 합니다.')
        return v

class CardUpdateRequest(BaseModel):
    bid: str
    bkey: str
    card: List[CardUpdate]

    @validator('bid')
    def validate_bid(cls, v):
        if len(v) != 2 or v not in ['EV', 'KP']:
            raise ValueError('bid는 "EV" 또는 "KP"이어야 합니다.')
        return v

    @validator('bkey')
    def validate_bkey(cls, v):
        if len(v) != 16:
            raise ValueError('bkey는 16자리여야 합니다.')
        return v

# /r2/card/update 엔드포인트
@app.post("/r2/card/update")
async def update_card(messages: str = Form(...)):
    try:
        # messages 필드의 JSON 데이터를 파싱하여 Pydantic 모델로 변환
        parsed_data = json.loads(messages)
        request_data = CardUpdateRequest(**parsed_data)

        # 요청받은 데이터를 로깅
        logger.info(f"Received request data: {request_data}")

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    # 실제 갱신 로직을 구현합니다. (예: DB 업데이트, 외부 API 호출 등)

    # 응답 데이터 생성 (예시로 더미 데이터를 반환)
    response_data = {
        "result": "0",  # 처리 성공
        "rdate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "reqcnt": len(request_data.card),
        "inscnt": 0,  # 신규 등록 건수 (예시로 0으로 설정)
        "updcnt": len(request_data.card),  # 갱신된 카드 수
        "dupcnt": 0,  # 중복된 카드 수 (예시로 0으로 설정)
        "limitcnt": 0,  # 요청 초과 건수 (예시로 0으로 설정)
        "errcnt": 0,  # 에러 발생 건수 (예시로 0으로 설정)
        "errlist": []  # 에러 목록
    }

    # 응답 데이터를 로깅
    logger.info(f"Response data: {response_data}")

    return JSONResponse(content=response_data)