from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from tracker.database import get_db, ApplicationTable
from tracker.routers.utils import get_token, verify_user_id, verify_application_owner
from tracker.auth.utils import verify_and_refresh_jwt
from jose import JWTError
from tracker.models.application import ApplicationIn, ApplicationResponse

router = APIRouter()

@router.post("/", response_model=ApplicationResponse)
async def create_application(application: ApplicationIn,
                             Authorization: str = Header(..., description="Bearer token for authentication"),
                             db: AsyncSession = Depends(get_db)):
    token = get_token(Authorization)

    try:
        decoded_token = verify_and_refresh_jwt(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e))

    username = decoded_token["username"]

    await verify_user_id(db, application.user_id, username)

    new_application = ApplicationTable(
        user_id=application.user_id,
        company_name=application.company_name,
        position_title=application.position_title,
        status=application.status,
        notes=application.notes,
        date_applied=application.date_applied,
        posting_url=application.posting_url,
        rejection_reason=None,
        rejection_date=None
    )

    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)

    return {
        "application": new_application,
        "new_token": decoded_token["new_token"],
        "token_type": "bearer"
    }


    
@router.delete("/{application_id}/")
async def delete_application(application_id: int,
                              Authorization: str = Header(..., description="Bearer token for authentication"),
                              db: AsyncSession = Depends(get_db)):
    token = get_token(Authorization)

    try:
        decoded_token = verify_and_refresh_jwt(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e))

    username = decoded_token["username"]
    
    application = await db.get(ApplicationTable, application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Application not found")

    await verify_application_owner(db, application.user_id, username)

    await db.delete(application)
    await db.commit()

    return {
        "message": "Application deleted successfully",
        "new_token": decoded_token["new_token"],
        "token_type": "bearer"
    }