import jwt
import uuid
import logging
from passlib.context import CryptContext
from datetime import timedelta, datetime
from itsdangerous import URLSafeSerializer

from src.config import Config


PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"])

SERIALIZER = URLSafeSerializer(secret_key=Config.JWT_SECRET, salt="email-verification")

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    hash = PASSWORD_CONTEXT.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return PASSWORD_CONTEXT.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)


def create_url_token(data: dict):
    token = SERIALIZER.dumps(data, salt="email-verification")

    return token 


def decode_url_token(token: str):
    try:
        token_data = SERIALIZER.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))
