from datetime import timedelta, datetime

import bcrypt
import jwt

from core.config import settings


# private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."

def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_time_delta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_time_delta:
        expire = now + expire_time_delta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithm)
    return decoded


hash_password = lambda pwd: bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
check_password = lambda pwd, hashed_pwd: bcrypt.checkpw(pwd.encode(), hashed_pwd)

# def hash_password(password: str) -> bytes:
#     salt = bcrypt.gensalt()
#     pwd_bytes: bytes = password.encode()
#     return bcrypt.hashpw(pwd_bytes, salt)
