from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional
import pycountry


class UserBase(BaseModel):
    login: str = Field(..., min_length=5, max_length=15, description="User login")
    password: str = Field(..., min_length=5, max_length=15, description="User password")
    description: Optional[str] = Field(
        None, description="User description", max_length=100
    )
    gender: Optional[int] = Field(None, description="User gender (1-male)", ge=0, le=1)
    birthday: Optional[date] = Field(
        None, description="User birthday in DD-MM-YYYY format"
    )
    country: Optional[str] = Field(None, description="User country")

    @field_validator("birthday", mode="before")
    def parse_birthday(cls, value):
        if value is None:
            return value
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in DD-MM-YYYY format")

    @field_validator("country")
    def validate_country(cls, value):
        if value is None:
            return value
        if not pycountry.countries.get(name=value):
            raise ValueError(f"{value} is not a valid country")
        return value


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int = Field(..., description="Unique user id")
    login: str
    password: bytes
    description: str | None
    gender: int
    birthday: date
    country: str
    date_created: datetime

    class Config:
        from_attributes = True


class UserShortResponse(BaseModel):
    login: str

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int = Field(..., description="Total number of users")


class UserUpdateLogin(BaseModel):
    new_login: str = Field(..., min_length=5, max_length=15, description="User login")


class UserUpdatePassword(BaseModel):
    old_password: str = Field(
        ..., min_length=5, max_length=15, description="User old password"
    )
    new_password: str = Field(
        ..., min_length=5, max_length=15, description="User new password"
    )


class UserUpdateDescription(BaseModel):
    new_description: Optional[str] = Field(
        None, description="User description", max_length=100
    )


class UserUpdateGender(BaseModel):
    new_gender: int = Field(..., description="User gender (1-male)", ge=0, le=1)


class UserUpdateBirthday(BaseModel):
    new_birthday: date = Field(..., description="User birthday in YYYY-MM-DD format")


class UserUpdateCountry(BaseModel):
    new_country: str = Field(..., description="User country")

    @field_validator("new_country")
    def validate_country(cls, value):
        if value is None:
            return value
        if not pycountry.countries.get(name=value):
            raise ValueError(f"{value} is not a valid country")
        return value


class UserLoginSchema(BaseModel):
    login: str
    password: str


class UserAuthSchema(BaseModel):
    # model_config = ConfigDict(strict=True)
    id: int | None = None
    login: str
