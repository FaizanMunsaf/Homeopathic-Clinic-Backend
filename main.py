from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config.security import authenticate_docs_credentials, ensure_docs_credentials
from fastapi.middleware.cors import CORSMiddleware

from api.health import router as health_router
from api.user import router as user_router

DOCS_USERNAME, DOCS_PASSWORD = ensure_docs_credentials()

app = FastAPI(
    title="Homeopathic Backend",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)
app.include_router(health_router)
app.include_router(user_router)

security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Homeopathic Backend API is running"}


@app.get("/docs", include_in_schema=False)
def swagger_docs(
    request: Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> HTMLResponse:
    authenticate_docs_credentials(credentials, DOCS_USERNAME, DOCS_PASSWORD)
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - Swagger UI",
    )


@app.get("/redoc", include_in_schema=False)
def redoc_docs(
    request: Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> HTMLResponse:
    authenticate_docs_credentials(credentials, DOCS_USERNAME, DOCS_PASSWORD)
    return get_redoc_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - ReDoc",
    )

# uvicorn main:app --reload --host