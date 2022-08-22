from .auth import user_router, auth_router
from .directors_router import directors_router
from .genres_router import genres_router
from .movies_router import movies_router

__all__ = [
    'genres_router',
    'directors_router',
    'movies_router',
    'auth_router',
    'user_router'
]