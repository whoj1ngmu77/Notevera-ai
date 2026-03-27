"""
Notevera AI – Authentication routes (signup, login, me)
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import bcrypt as _bcrypt_lib
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

from database import database
from models.tables import users, settings as settings_table

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("SECRET_KEY", "notevera-super-secret-key-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


security = HTTPBearer()


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return dict(user._mapping)


@router.post("/signup")
async def signup(req: SignupRequest):
    # Check if email already exists
    query = users.select().where(users.c.email == req.email)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = _bcrypt_lib.hashpw(req.password.encode(), _bcrypt_lib.gensalt()).decode()
    insert_query = users.insert().values(
        name=req.name, email=req.email, password_hash=hashed
    )
    user_id = await database.execute(insert_query)

    # Create default settings
    await database.execute(
        settings_table.insert().values(user_id=user_id, theme="dark")
    )

    token = create_token(user_id)
    return {
        "token": token,
        "user": {"id": str(user_id), "name": req.name, "email": req.email, "avatar": ""},
    }


@router.post("/login")
async def login(req: LoginRequest):
    query = users.select().where(users.c.email == req.email)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    u = dict(user._mapping)
    ph = u["password_hash"]
    ph_bytes = ph.encode() if isinstance(ph, str) else ph
    if not _bcrypt_lib.checkpw(req.password.encode(), ph_bytes):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(u["id"])
    return {
        "token": token,
        "user": {
            "id": str(u["id"]),
            "name": u["name"],
            "email": u["email"],
            "avatar": u.get("avatar", ""),
        },
    }


@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user["id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "avatar": current_user.get("avatar", ""),
    }
