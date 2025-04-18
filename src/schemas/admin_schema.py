from uuid import UUID

from pydantic import BaseModel


class SUsersBasic(BaseModel):
    id: UUID
    email: str
    fio: str

class SConfirm(BaseModel):
    roles: list[str]