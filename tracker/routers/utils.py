from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tracker.database import UserTable



def get_token(auth_header: str) -> str:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalido or missing Authorization header")
    
    return auth_header.split(" ")[1]

async def verify_application_owner(db: AsyncSession, application_user_id: int, username: str):
    user = await db.execute(
        select(UserTable).where(UserTable.username == username)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")
    
    if application_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="User ID does not match the token")

    return True