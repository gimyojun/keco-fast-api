# models.py
from pydantic import BaseModel, validator
from typing import List

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

# 카드 업데이트 모델
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