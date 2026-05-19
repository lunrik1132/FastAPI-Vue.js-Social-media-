from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
from .routes import (
    users_router,
    posts_router,
    likes_router,
    comments_router,
    auth_router,
    friendship_router,
    chat_router,
    message_router,
    websockets_router,
)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static", StaticFiles(directory=settings.static_dir, html=True), name="static"
)

app.include_router(users_router)
app.include_router(friendship_router)
app.include_router(posts_router)
app.include_router(likes_router)
app.include_router(comments_router)
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(auth_router)
app.include_router(websockets_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "message": "Welcome to blog",
        "docs": "api/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
