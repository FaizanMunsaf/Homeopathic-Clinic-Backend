import os
import secrets
import hmac

from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def ensure_docs_credentials() -> tuple[str, str]:
    username = settings.docs_username or os.getenv("DOCS_USERNAME") or "admin"
    password = settings.docs_password or os.getenv("DOCS_PASSWORD")

    if not password:
        password = "changeme"

    os.environ["DOCS_USERNAME"] = username
    os.environ["DOCS_PASSWORD"] = password
    return username, password


def authenticate_docs_credentials(
    credentials: HTTPBasicCredentials,
    docs_username: str,
    docs_password: str,
) -> None:
    correct_username = secrets.compare_digest(credentials.username, docs_username)
    correct_password = secrets.compare_digest(credentials.password, docs_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def _peppered_password(password: str) -> str:
    secret = settings.password_secret_key
    if not secret:
        raise RuntimeError(
            "PASSWORD_SECRET_KEY must be set in .env or the environment to hash passwords"
        )
    return hmac.new(secret.encode(), password.encode(), "sha256").hexdigest()


def hash_password(password: str) -> str:
    return pwd_context.hash(_peppered_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_peppered_password(plain_password), hashed_password)
