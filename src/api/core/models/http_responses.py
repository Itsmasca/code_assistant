from pydantic import BaseModel

class ResponseWithDetail(BaseModel):
    detail: str