from pydantic import BaseModel

class ResponseBase(BaseModel):
    success:bool
    log:str

class WSCommonRequestBase(BaseModel):
    event:str
    
class WSCommonResponseBase(ResponseBase):
    event:str
    # success:bool
