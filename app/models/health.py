from pydantic import BaseModel


class Health(BaseModel):
    status: str = "ok"
    version: str
