from pathlib import Path
import os
import sys
import threading
import time
import webbrowser

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
# Make sure imports work whether the app runs as a module or a script.
for path in (PROJECT_ROOT, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.append(str(path))


from src.app.controller.auth_controller import get_current_user, router as auth_router
from src.app.controller.role_controller import router as role_router


DOCS_URL = "http://127.0.0.1:8001/docs"
BROWSER_CANDIDATES = [
    "C://Program Files//Google//Chrome//Application//chrome.exe",
    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
]


def load_environment() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)


def create_app() -> FastAPI:
    load_environment()

    app = FastAPI(
        title="POS API",
        version="1.0.0",
        description="API para la gestion de pedidos",
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.9:5173",
        "https://api.seustech.com",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        # DevTunnels cambia el subdominio; permitir cualquier túnel 5173.
        allow_origin_regex=r"https://.*-5173\.use\.devtunnels\.ms",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    app.include_router(auth_router)
    app.include_router(role_router, dependencies=[Depends(get_current_user)])

    # Respuesta para preflight CORS (OPTIONS) sin autenticacion.
    @app.options("/{full_path:path}")
    def preflight_handler(full_path: str) -> Response:
        return Response(status_code=200)

    @app.get("/")
    def root():
        return {"mensaje": "API POS en ejecucion"}

    return app


app = create_app()


def open_docs_in_browser() -> None:
    time.sleep(1)

    for path in BROWSER_CANDIDATES:
        if os.path.exists(path):
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(path))
            webbrowser.get("chrome").open_new(DOCS_URL)
            return

    webbrowser.open_new(DOCS_URL)


def main() -> None:
    threading.Thread(target=open_docs_in_browser, daemon=True).start()

    import uvicorn

    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )


if __name__ == "__main__":
    main()
