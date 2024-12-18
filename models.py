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




class CardListRequest(BaseModel):
    bid: str
    bkey: str
    kind: str

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

    @validator('kind')
    def validate_kind(cls, v):
        if v not in ['1', '2', '3']:
            raise ValueError('kind는 "1", "2", "3" 중 하나여야 합니다.')
        return v

class Card(BaseModel):
    bid: str
    no: str
    stop: str
    regdate: str
    upddate: str

class Trade(BaseModel):
    no: str
    sid: str
    cid: str
    tbid: str
    tsdt: str
    tedt: str
    btid: str = None
    pow: int
    mon: int
    bprice: float = None
    tbprice: float = None
    bmon: int = None

    @validator('no')
    def validate_no(cls, v):
        if len(v) != 16 or not v.isdigit():
            raise ValueError('회원카드는 16자리 숫자형식입니다.')
        return v

    @validator('sid')
    def validate_sid(cls, v):
        if len(v) != 6 or not v.isdigit():
            raise ValueError('충전소ID는 6자리 숫자형식입니다.')
        return v

    @validator('cid')
    def validate_cid(cls, v):
        if len(v) != 2 or not v.isdigit():
            raise ValueError('충전기ID는 2자리 숫자형식입니다.')
        return v

    @validator('tsdt', 'tedt')
    def validate_datetime(cls, v):
        if len(v) != 14 or not v.isdigit():
            raise ValueError('날짜는 14자리 숫자형식이어야 합니다.')
        return v

class TradeRegiRequest(BaseModel):
    bid: str
    bkey: str
    trade: List[Trade]

    @validator('bid')
    def validate_bid(cls, v):
        if len(v) != 2 or v not in ['EV', 'KP']:
            raise ValueError('bid는 "EV" 또는 "KP"이어야 합니다.')
        return v

class Use(BaseModel):
    sid: str
    cid: str
    tbid: str
    tsdt: str
    tedt: str
    pow: int
    mon: int
    rcvdate: str = None

    @validator('sid')
    def validate_sid(cls, v):
        if len(v) != 6 or not v.isdigit():
            raise ValueError('충전소ID는 6자리 숫자형식입니��.')
        return v

    @validator('cid')
    def validate_cid(cls, v):
        if len(v) != 2 or not v.isdigit():
            raise ValueError('충전기ID는 2자리 숫자형식입니다.')
        return v

    @validator('tsdt', 'tedt', 'rcvdate')
    def validate_datetime(cls, v):
        if v and (len(v) != 14 or not v.isdigit()):
            raise ValueError('날짜는 14자리 숫자형식이어야 합니다.')
        return v

class UseRegiRequest(BaseModel):
    bid: str
    bkey: str
    use: List[Use]

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

class TradeListRequest(BaseModel):
    bid: str
    bkey: str
    kind: str

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

    @validator('kind')
    def validate_kind(cls, v):
        if v not in ['1', '2', '3']:
            raise ValueError('kind는 "1", "2", "3" 중 하나여야 합니다.')
        return v

class ChargerStatusRequest(BaseModel):
    bid: str
    bkey: str
    kind: str

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

    @validator('kind')
    def validate_kind(cls, v):
        if v not in ['1', '2', '3']:
            raise ValueError('kind는 "1", "2", "3" 중 하나여야 합니다.')
        return v

class ChargerStatusUpdateRequest(BaseModel):
    bid: str
    bkey: str
    cstat: List[dict]

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

    @validator('cstat')
    def validate_cstat(cls, v):
        for item in v:
            if 'sid' not in item or len(item['sid']) != 6:
                raise ValueError('sid는 6자리여야 합니다.')
            if 'cid' not in item or len(item['cid']) != 2:
                raise ValueError('cid는 2자리여야 합니다.')
            if 'status' not in item or item['status'] not in ['0', '1', '2', '3', '4', '5', '6']:
                raise ValueError('status는 "0", "1", "2", "3", "4", "5", "6" 중 하나여야 합니다.')
        return v

class ChargerInfoListRequest(BaseModel):
    bid: str
    bkey: str
    kind: str

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

    @validator('kind')
    def validate_kind(cls, v):
        if v not in ['1', '2', '3']:
            raise ValueError('kind는 "1", "2", "3" 중 하나여야 합니다.')
        return v
    
class ChargerStatusUpdateRequest(BaseModel):
    bid: str
    bkey: str
    cstat: List[dict]

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

    @validator('cstat')
    def validate_cstat(cls, v):
        for item in v:
            if 'sid' not in item or len(item['sid']) != 6:
                raise ValueError('sid는 6자리여야 합니다.')
            if 'cid' not in item or len(item['cid']) != 2:
                raise ValueError('cid는 2자리여야 합니다.')
            if 'status' not in item or item['status'] not in ['0', '1', '2', '3', '4', '5', '6']:
                raise ValueError('status는 "0", "1", "2", "3", "4", "5", "6" 중 하나여야 합니다.')
        return v

class ChargerQRRequest(BaseModel):
    bid: str
    bkey: str
    pageno: int
    pagesize: int

class ChargingStationUpdate(BaseModel):
    spid: str
    csid: str = ""
    csnm: str
    daddr: str
    addr: str = ""
    addr_dtl: str = ""
    lat: str
    longi: str
    use_time: str
    show_yn: str
    spcsid: str
    park_fee_yn: str
    park_fee: str
    spcall: str
    member_yn: str
    open_yn: str
    use_yn: str
    postcd: str
    cs_div: str
    sido: str
    sigungu: str
    oper_st_ymd: str
    oper_end_ymd: str
    plusdr_yn: str = ""
    me_cs_id: str

    @validator('spid')
    def validate_spid(cls, v):
        if len(v) != 3:
            raise ValueError('spid는 3자리여야 합니다.')
        return v

class ChargingStationUpdateRequest(BaseModel):
    spkey: str
    list: List[ChargingStationUpdate]

class ChargerUpdate(BaseModel):
    spid: str
    csid: str
    cpid: str
    cpnm: str
    use_time: str
    open_yn: str
    show_yn: str
    spcsid: str = ""
    spcpid: str = ""
    charge_ucost1: str
    charge_ucost2: str = ""
    charge_ucost3: str = ""
    use_yn: str
    oper_st_ymd: str
    oper_end_ymd: str
    outlet_cnt: str
    pnc_yn: str = "N"
    cpkw: str
    charge_div: str
    cp_div: str
    postcd: str
    cs_div: str
    outlet_div: str
    conn_div: str
    charge_kw: str
    service_div: str
    net_div: str
    auth_div: str
    compty_div: str
    ami_cert: str = ""
    reserv_yn: str = "N"
    qrid: str = ""
    me_cs_id: str
    me_cp_id: str

    @validator('spid')
    def validate_spid(cls, v):
        if len(v) != 3:
            raise ValueError('spid는 3자리여야 합니다.')
        return v

    @validator('open_yn', 'show_yn', 'use_yn', 'pnc_yn', 'reserv_yn')
    def validate_yn_fields(cls, v):
        if v not in ['Y', 'N']:
            raise ValueError('Y/N 필드는 "Y" 또는 "N"이어야 합니다.')
        return v

    @validator('oper_st_ymd', 'oper_end_ymd')
    def validate_oper_date(cls, v):
        if len(v) != 8 or not v.isdigit():
            raise ValueError('날짜는 8자리 숫자형식(YYYYMMDD)이어야 합니다.')
        return v

    @validator('me_cs_id')
    def validate_me_cs_id(cls, v):
        if len(v) != 6 or not v.isdigit():
            raise ValueError('환경부 충전소ID는 6자리 숫자여야 합니다.')
        return v

    @validator('me_cp_id')
    def validate_me_cp_id(cls, v):
        if len(v) != 2 or not v.isdigit():
            raise ValueError('환경부 충전기ID는 2자리 숫자여야 합니다.')
        return v

class ChargerUpdateRequest(BaseModel):
    spkey: str
    list: List[ChargerUpdate]

