# main.py
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
import json
from pathlib import Path

from models import Message, CardUpdateRequest, CardListRequest, TradeRegiRequest, UseRegiRequest, TradeListRequest, ChargerStatusRequest, ChargerInfoListRequest, ChargerStatusUpdateRequest  # models.py에서 임포트

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

@app.post("/r2/card/list")
async def list_card(messages: str = Form(...)):
    try:
        # 클라이언트가 보낸 messages 필드의 JSON 데이터를 파싱하여 Pydantic 모델로 변환
        parsed_data = json.loads(messages)
        request_data = CardListRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    # card_list_kind1.json 파일 경로
    file_path = Path(__file__).parent / 'card_listall_kind1_response_0929.json'

    try:
        # JSON 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        # 응답 데이터를 로깅
        logger.info(f"Response data: {file_data}")

        # 파일 내용을 그대로 반환
        return JSONResponse(content=file_data)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Requested data not found.")
    except Exception as e:
        logger.error(f"Error reading the file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/r2/trade/regi")
async def trade_regi(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = TradeRegiRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    response_data = {
        "result": "0",
        "rdate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "reqcnt": len(request_data.trade),
        "inscnt": len(request_data.trade),  # 실제 등록된 건수로 수정 필요
        "dupcnt": 0,  # 중복 건수로 수정 필요
        "limitcnt": 0,
        "errcnt": 0,
        "errlist": []
    }
    logger.info(f"Response data: {response_data}")

    return JSONResponse(content=response_data)

@app.post("/r2/use/regi")
async def use_regi(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = UseRegiRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    response_data = {
        "result": "0",
        "rdate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "reqcnt": len(request_data.use),
        "inscnt": len(request_data.use),  # 실제 등록된 건수로 수정 필요
        "dupcnt": 0,  # 중복 건수로 수정 필요
        "limitcnt": 0,
        "errcnt": 0,
        "errlist": []
    }
    logger.info(f"Response data: {response_data}")

    return JSONResponse(content=response_data)

@app.post("/r2/trade/listall")
async def trade_list(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = TradeListRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    # pageno에 따라 파일 경로 설정
    file_map = {
        "1": 'trade_list_kind1_response.json',
        "2": 'trade_list_kind1_response2.json',
        "3": 'trade_list_kind1_response3.json',
        "4": 'trade_list_kind1_response4.json'
    }

    # pageno 가져오기
    pageno = str(parsed_data.get("pageno", "1"))
    
    if pageno not in file_map:
        logger.error(f"Invalid pageno: {pageno}")
        raise HTTPException(status_code=400, detail="Invalid pageno")

    file_name = file_map[pageno]
    file_path = Path(__file__).parent / file_name

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        logger.info(f"Response data for pageno {pageno}: {file_data}")

        return JSONResponse(content=file_data)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Requested data not found.")
    except Exception as e:
        logger.error(f"Error reading the file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
@app.post("/r2/charger/info/list")
async def charger_info_list(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = ChargerInfoListRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    file_path = Path(__file__).parent / 'charger_info_list_response.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        logger.info(f"Response data: {file_data}")

        return JSONResponse(content=file_data)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Requested data not found.")
    except Exception as e:
        logger.error(f"Error reading the file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/r2/charger/status/update")
async def charger_status_update(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = ChargerStatusUpdateRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    response_data = {
        "result": "0",
        "rdate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "reqcnt": len(request_data.cstat),
        "updcnt": len(request_data.cstat),  # 실제 갱신된 건수로 수정 필요
        "limitcnt": 0,
        "errcnt": 0,
        "errlist": []
    }
    logger.info(f"Response data: {response_data}")

    return JSONResponse(content=response_data)

@app.post("/r2/charger/status/list")
async def charger_status_list(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = ChargerStatusRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    file_path = Path(__file__).parent / 'charger_status_list_response.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        logger.info(f"Response data: {file_data}")

        return JSONResponse(content=file_data)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Requested data not found.")
    except Exception as e:
        logger.error(f"Error reading the file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/r2/charger/info/listall")
async def charger_info_listall(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = ChargerInfoListRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    # pageno에 따라 파일 경로 설정
    file_map = {
        "1": 'charger_info_list_response1.json',
        "2": 'charger_info_list_response2.json',
        "3": 'charger_info_list_response3.json'
    }

    # pageno 가져오기
    pageno = str(parsed_data.get("pageno", "1"))
    
    if pageno not in file_map:
        logger.error(f"Invalid pageno: {pageno}")
        raise HTTPException(status_code=400, detail="Invalid pageno")

    file_name = file_map[pageno]
    file_path = Path(__file__).parent / file_name

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        logger.info(f"Response data for pageno {pageno}: {file_data}")

        return JSONResponse(content=file_data)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Requested data not found.")
    except Exception as e:
        logger.error(f"Error reading the file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/r2/trade/list")
async def trade_list(messages: str = Form(...)):
    try:
        parsed_data = json.loads(messages)
        request_data = TradeListRequest(**parsed_data)
        logger.info(f"Received request data: {request_data}")
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    file_path = Path(__file__).parent / 'trade_listall_kind1_response_1027_1028.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        logger.info(f"Response data: {file_data}")

        return JSONResponse(content=file_data)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Requested data not found.")
    except Exception as e:
        logger.error(f"Error reading the file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
