from .users import router as users_router
from .posts import router as posts_router
from .likes import router as likes_router
from .comments import router as comments_router
from .auth import router as auth_router
from .friendship import router as friendship_router
from .chat import router as chat_router
from .message import router as message_router
from .websockets import router as websockets_router

__all__ = [
    "users_router",
    "posts_router",
    "likes_router",
    "comments_router",
    "auth_router",
    "friendship_router",
    "chat_router",
    "message_router",
]
