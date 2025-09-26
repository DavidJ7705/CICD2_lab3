# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, conint, Field

class User(BaseModel):
    user_id: int
    student_id: str = Field(..., pattern=r"^S\d{7}$") # regex got replaced by pattern in new version of pydancti
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    age: conint(gt=18)
