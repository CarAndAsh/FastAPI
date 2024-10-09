from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    # username: str = Field(..., min_length=1, max_length=20)
    username: Annotated[str, MinLen(1), MaxLen(20)]
    email: EmailStr
