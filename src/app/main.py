from pathlib import Path
import os
import secrets
import sys
import threading
import time
import webbrowser

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

# Make sure imports work whether the app runs as a module or a script.
for path in (PROJECT_ROOT, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.append(str(path))

import app
from src.app.controller.auth_controller import get_current_user, router as auth_router
from src.app.controller.role_controller import router as role_router

DOCS_URL = "http://127.0.0.1:8001/docs"
DOCS_SECURITY = HTTPBasic()

BROWSER_CANDIDATES = [
    "C://Program Files//Google//Chrome//Application//chrome.exe",
    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
]


def load_environment() -> None:
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)


def verify_docs_access(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(DOCS_SECURITY),
) -> None:
    username = os.getenv("DOCS_USERNAME", "")
    password = os.getenv("DOCS_PASSWORD", "")
    allowed_ips = {
        ip.strip()
        for ip in os.getenv("DOCS_ALLOWED_IPS", "127.0.0.1,::1").split(",")
        if ip.strip()
    }

    client_host = request.client.host if request.client else ""
    if client_host not in allowed_ips:
        # 404 to avoid exposing that docs exist.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    valid_user = secrets.compare_digest(credentials.username, username)
    valid_pass = secrets.compare_digest(credentials.password, password)

    if not (valid_user and valid_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )


def create_app() -> FastAPI:
    load_environment()

    app = FastAPI(
        title="POS API",
        version="1.0.0",
        description="API para la gestion de pedidos",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.9:5173",
        "https://pos.seustech.com",
        "http://192.168.1.9:4173"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(
        role_router,
        dependencies=[Depends(get_current_user)]
    )

    # Respuesta para preflight CORS (OPTIONS) sin autenticacion
    @app.options("/{full_path:path}")
    def preflight_handler(full_path: str) -> Response:
        return Response(status_code=200)

    @app.get("/")
    def root():
        return {"mensaje": "API POS en ejecucion"}

    @app.get("/openapi.json", include_in_schema=False)
    def openapi_schema(_: None = Depends(verify_docs_access)):
        return get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

    @app.get("/docs", include_in_schema=False)
    def protected_docs(_: None = Depends(verify_docs_access)):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=f"{app.title} - Swagger UI",
        )

    return app


app = create_app()


def open_docs_in_browser() -> None:
    time.sleep(1)

    for path in BROWSER_CANDIDATES:
        if os.path.exists(path):
            webbrowser.register(
                "chrome",
                None,
                webbrowser.BackgroundBrowser(path)
            )
            webbrowser.get("chrome").open_new(DOCS_URL)
            return

    webbrowser.open_new(DOCS_URL)


def main() -> None:
    threading.Thread(
        target=open_docs_in_browser,
        daemon=True
    ).start()

    import uvicorn

    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )


if __name__ == "__main__":
    main()
