import os
import secrets
from pathlib import Path

from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials

from config.settings import settings

ENV_FILE = Path(".env")


def ensure_docs_credentials() -> tuple[str, str]:
    username = settings.docs_username or "admin"
    password = settings.docs_password

    if not password:
        password = secrets.token_urlsafe(18)

    if not ENV_FILE.exists():
        ENV_FILE.write_text(
            f"DOCS_USERNAME={username}\nDOCS_PASSWORD={password}\n",
            encoding="utf-8",
        )
    else:
        content = ENV_FILE.read_text(encoding="utf-8")
        if "DOCS_USERNAME=" not in content:
            content += f"\nDOCS_USERNAME={username}\n"
        if "DOCS_PASSWORD=" not in content:
            content += f"DOCS_PASSWORD={password}\n"
        ENV_FILE.write_text(content, encoding="utf-8")

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
