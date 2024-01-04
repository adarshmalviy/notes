from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_throttling import ThrottlingMiddleware
from app.routers import notes, user


def create_app():  # App creation
    app = FastAPI(
        title="Speer Technologies Assignment",
        description="Documentation of Notes API",
    )

    # CORS handling
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Throttling Middleware
    # app.add_middleware(ThrottlingMiddleware, limit=1000, window=60)

    # Adding API routers

    app.include_router(
        user.router,
        prefix="/api/auth",
        tags=["User Endpoints"]
    )

    app.include_router(
        notes.router,
        prefix="/api/notes",
        tags=["Note Endpoints"]
    )
    
    return app
