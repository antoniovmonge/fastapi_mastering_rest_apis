from fastapi import APIRouter

from src.api.v1 import general, posts

router = APIRouter()

router.include_router(posts.router, prefix="/posts", tags=["posts"])
router.include_router(general.router, prefix="/general", tags=["general"])
