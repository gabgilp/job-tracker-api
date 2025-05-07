from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


def get_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalido or missing Authorization header")
    
    return auth_header.split(" ")[1]

async def get_user_from_db(db: AsyncSession, username: str):
    result = await db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": username})
    return result.fetchone()