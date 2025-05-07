from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text



def get_token(auth_header: str) -> str:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalido or missing Authorization header")
    
    return auth_header.split(" ")[1]

async def get_user_from_db(db: AsyncSession, username: str):
    result = await db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": username})
    return result.fetchone()

async def verify_user_id(db: AsyncSession, user_id: int, username: str):

    user = await get_user_from_db(db, username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")
    if user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="User ID does not match the token")

    return True