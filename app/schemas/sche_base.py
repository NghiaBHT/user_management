from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    code: str = ''
    message: str = ''

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = '000'
        self.message = 'Thành công'
        return self


class DataResponse(ResponseSchemaBase, Generic[T]):
    data: Optional[T] = None

    model_config = {
        'arbitrary_types_allowed': True
    }

    def custom_response(self, code: str, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T):
        self.code = '000'
        self.message = 'Thành công'
        self.data = data
        return self


class CustomException(Exception):
    def __init__(self, http_code: int = 500, code: Optional[str] = None, message: Optional[str] = None):
        self.http_code = http_code
        self.code = code if code else str(http_code)
        self.message = message or "Internal Server Error"

    def __str__(self):
        return f"[{self.http_code}] {self.code}: {self.message}"
