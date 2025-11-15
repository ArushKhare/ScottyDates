# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True


class ProfileCreate(BaseModel):
    age: int
    gender: str
    major: str
    class_year: int
    campus: str
    interests: List[str]
    bio: str


class ProfileOut(ProfileCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class MatchOut(BaseModel):
    user_id: int
    other_user_id: int
    score: float
    profile: ProfileOut


class MessageCreate(BaseModel):
    to_user_id: int
    text: str


class MessageOut(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    text: str
    created_at: datetime

    class Config:
        orm_mode = True


class AIChatHelperResponse(BaseModel):
    summary: str
    openers: List[str]
