from pydantic import BaseModel
from schemas.base import ResponseBase

class ReadDeckRequest(BaseModel):
    pass

class ReadDeckResponse(ResponseBase):
    pass

class ReadCardRequest(BaseModel):
    pass

class ReadCardResponse(ResponseBase):
    pass