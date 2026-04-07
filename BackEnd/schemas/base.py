from pydantic import BaseModel

class ResponseBase(BaseModel):
    success:bool
    log:str

class WSRequestBase(BaseModel):
    event:str=None
    
class WSResponseBase(ResponseBase):
    event:str=None
