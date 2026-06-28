import os
import secrets

from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials

from config.settings import settings


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
