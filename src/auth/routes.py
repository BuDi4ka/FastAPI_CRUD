from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime

from .schemas import (
    UserCreateModel,
    UserResponseModel,
    UserLoginModel,
    UserBooksModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetModel,
)
from .service import UserService
from .utils import (
    create_access_token,
    verify_password,
    create_url_token,
    decode_url_token,
    generate_password_hash
)
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)

from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, UserNotFound, InvalidToken, InvalidCredentials
from src.mail import mail, create_message
from src.config import Config


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post("/send-mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"

    message = create_message(recipients=emails, subject="Welcome", body=html)

    await mail.send_message(message)

    return {"message": "Email sent successfully"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    else:
        new_user = await user_service.create_user(user_data, session)

    token = create_url_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@auth_router.post("/login")
async def login(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()

    return {}


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(content={"message": "Logged out successfully"})


@auth_router.post("/password-reset-request")
async def request_password_reset(
    reset_data: PasswordResetRequestModel, 
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    # Get authenticated user's email from token
    authenticated_user_email = token_details.get("user")["email"]
    
    # Verify the request is for the authenticated user
    if authenticated_user_email != reset_data.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only request password reset for your own account"
        )

    user = await user_service.get_user_by_email(reset_data.email, session)
    if not user:
        raise UserNotFound()

    # Create token with email
    token = create_url_token({"email": user.email})

    # Create reset link
    reset_link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset/{token}"

    # Create email content
    html_message = f"""
    <h1>Password Reset Request</h1>
    <p>Click this <a href="{reset_link}">link</a> to reset your password.</p>
    <p>If you didn't request this, please ignore this email.</p>
    <p>{token}</p>
    """

    # Send email
    message = create_message(
        recipients=[user.email], subject="Password Reset Request", body=html_message
    )
    await mail.send_message(message)

    return JSONResponse(
        content={"message": "If account exists, password reset link has been sent"},
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset/{token}")
async def reset_password(
    token: str,
    password_data: PasswordResetModel,
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    # Get authenticated user's email from token
    authenticated_user_email = token_details.get("user")["email"]
    
    # Decode reset token
    reset_token_data = decode_url_token(token)
    user_email = reset_token_data.get("email")

    if not user_email:
        raise InvalidToken()

    # Verify the reset is for the authenticated user
    if authenticated_user_email != user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only reset password for your own account"
        )

    # Verify passwords match
    if password_data.password != password_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Passwords don't match"
        )

    # Get user and update password
    user = await user_service.get_user_by_email(user_email, session)
    if not user:
        raise UserNotFound()

    # Update password
    new_password_hash = generate_password_hash(password_data.password)
    await user_service.update_user(
        user, 
        {"password_hash": new_password_hash}, 
        session
    )

    return JSONResponse(
        content={"message": "Password successfully reset"},
        status_code=status.HTTP_200_OK,
    )
