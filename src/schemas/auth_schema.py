from uuid import UUID

from pydantic import BaseModel


class SRegister(BaseModel):
    email: str
    fio: str
    password: str

class SLogin(BaseModel):
    email: str
    password: str

class SUser(BaseModel):
    id: UUID
    fio: str
    email: str
