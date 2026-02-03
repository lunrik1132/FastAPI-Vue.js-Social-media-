from fastapi import APIRouter, Depends, status, Query, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import glob
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..services.user_service import UserService
from ..services.file_service import save_user_image
from ..schemas.user import (
    UserResponse,
    UserListResponse,
    UserCreate,
    UserUpdateLogin,
    UserUpdatePassword,
    UserUpdateDescription,
    UserUpdateGender,
    UserUpdateBirthday,
    UserUpdateCountry,
)
from ..schemas.user import UserAuthSchema
from ..auth import auth

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=UserListResponse, status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_users()


@router.get(
    "/id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)


@router.get(
    "/login/{user_login}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def get_user_by_login(user_login: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_login(user_login)


@router.get("/search", response_model=UserListResponse)
def search_users_by_login(
    query: str = Query(..., min_length=1), db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.get_all_users_by_login(query)


@router.post("", status_code=status.HTTP_200_OK)
def add_user(user_data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    new_user = service.create_user(user_data)
    return {"message": "User added", "new_user": new_user}


@router.delete("", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    deleted_user = service.delete_user(user_id)
    return {"message": "User deleted", "deleted_user": deleted_user}


@router.patch("/login", status_code=status.HTTP_200_OK)
def update_user_login(
    login_data: UserUpdateLogin,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated_user = service.update_user_login(
        user_id=user.id, new_login=login_data.new_login
    )
    return {"message": "User description updated", "updated_user": updated_user}


@router.patch("/password", status_code=status.HTTP_200_OK)
def update_user_password(
    password_data: UserUpdatePassword,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated_user = service.update_user_password(
        user_id=user.id,
        old_password=password_data.old_password,
        new_password=password_data.new_password,
    )
    return {"message": "User description updated", "updated_user": updated_user}


@router.patch("/description", status_code=status.HTTP_200_OK)
def update_user_description(
    description_data: UserUpdateDescription,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated_user = service.update_user_description(
        user_id=user.id, new_description=description_data.new_description
    )
    return {"message": "User description updated", "updated_user": updated_user}


@router.patch("/gender", status_code=status.HTTP_200_OK)
def update_user_gender(
    gender_data: UserUpdateGender,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated_user = service.update_user_gender(
        user_id=user.id, new_gender=gender_data.new_gender
    )
    return {"message": "User description updated", "updated_user": updated_user}


@router.patch("/birthday", status_code=status.HTTP_200_OK)
def update_user_birthday(
    birthday_data: UserUpdateBirthday,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated_user = service.update_user_birthday(
        user_id=user.id, new_birthday=birthday_data
    )
    return {"message": "User description updated", "updated_user": updated_user}


@router.patch("/country", status_code=status.HTTP_200_OK)
def update_user_country(
    country_data: UserUpdateCountry,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated_user = service.update_user_country(
        user_id=user.id, new_country=country_data.new_country
    )
    return {"message": "User description updated", "updated_user": updated_user}


@router.patch("/imageurl", status_code=status.HTTP_200_OK)
def update_user_imageURL(
    user_id: int,
    new_url: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated_user = service.update_user_url(user_id, new_url)
    return {"message": "User image url updated", "updated_user": updated_user}


@router.get("/{user_id}/avatar")
def get_avatar(user_id: int):
    images = glob.glob(f"static/images/{user_id}_image.*")
    default_path = Path("static/images/default_image.jpg")

    if images:
        return FileResponse(
            path=images[0],
            headers={
                "Cache-Control": "private, max-age=5",
            },
        )
    return FileResponse(
        path=default_path,
        headers={
            "Cache-Control": "private, max-age=5",
        },
    )


@router.get("/{user_id}/bgimage")
def get_bg_image(user_id: int):
    images = glob.glob(f"static/images/{user_id}_bgimage.*")
    default_path = Path("static/images/default_bgimage.jpg")

    if images:
        return FileResponse(
            path=images[0],
            headers={
                "Cache-Control": "private, max-age=5",
            },
        )
    return FileResponse(
        path=default_path,
        headers={
            "Cache-Control": "private, max-age=5",
        },
    )


@router.post("/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
):
    avatar_path = save_user_image(file=file, user_id=user.id, image_type="image")
    return {"avatar": avatar_path}


@router.post("/bgimage")
def upload_background(
    file: UploadFile = File(...),
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
):
    bg_path = save_user_image(file=file, user_id=user.id, image_type="bgimage")
    return {"bgImage": bg_path}
