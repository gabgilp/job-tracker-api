from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from tracker.database import get_db, ApplicationTable
from tracker.routers.utils import get_token, verify_user_id, verify_application_owner
from tracker.auth.utils import verify_and_refresh_jwt
from jose import JWTError
from tracker.models.application import ApplicationIn, ApplicationResponse, ApplicationToModify

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

@router.put("/{application_id}/", response_model=ApplicationResponse)
async def update_application(application_id: int,
                             application: ApplicationToModify,
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

    application_in_db = await db.get(ApplicationTable, application_id)
    if not application_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Application not found")
    await verify_application_owner(db, application_in_db.user_id, username)

    application_in_db.company_name = application.company_name
    application_in_db.position_title = application.position_title
    application_in_db.status = application.status
    application_in_db.notes = application.notes
    application_in_db.date_applied = application.date_applied
    application_in_db.posting_url = application.posting_url
    application_in_db.rejection_reason = application.rejection_reason
    application_in_db.rejection_date = application.rejection_date
    await db.commit()
    await db.refresh(application_in_db)
    return {
        "application": application_in_db,
        "new_token": decoded_token["new_token"],
        "token_type": "bearer"
    }

@router.get("/{application_id}/", response_model=ApplicationResponse)
async def get_application(application_id: int,
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

    return {
        "application": application,
        "new_token": decoded_token["new_token"],
        "token_type": "bearer"
    }