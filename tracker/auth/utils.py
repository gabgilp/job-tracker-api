from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from tracker.config import config


ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta if expires_delta else datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_jwt_for_user(username: str):
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def verify_and_refresh_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if username is None:
            raise JWTError("Invalid token")
        if exp is None:
            raise JWTError("Token has no expiration time")
        if datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise JWTError("Token has expired")
        
        if datetime.fromtimestamp(exp, tz=timezone.utc) - datetime.now(timezone.utc) < timedelta(minutes=10):
            new_token = create_access_token(
                data={"sub": username}, expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        else:
            new_token = token
        return {"username": username, "new_token": new_token}
    except JWTError as e:
        raise JWTError(f"Token verification failed: {e}")