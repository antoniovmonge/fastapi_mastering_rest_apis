from fastapi import APIRouter, HTTPException

from src.schemas.posts import (
    CommentSchema,
    CreateCommentSchema,
    CreatePostSchema,
    PostSchema,
    PostWithCommentsSchema,
)

router = APIRouter()

post_table = {}
comment_table = {}


def find_post(id: int):
    return post_table.get(id)


@router.post("/", response_model=PostSchema, status_code=201)
async def create_post(post: CreatePostSchema):
    id = len(post_table) + 1
    new_post = {**post.model_dump(), "id": id}
    post_table[id] = new_post
    return new_post


@router.get("/", response_model=list[PostSchema])
async def get_all_posts():
    """Read all Posts"""
    return list(post_table.values())


@router.post("/comments/", response_model=CommentSchema, status_code=201)
async def create_comment(comment: CreateCommentSchema):
    """Create a Comment on a Post"""
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    id = len(comment_table) + 1
    new_comment = {**comment.model_dump(), "id": id}
    comment_table[id] = new_comment
    return new_comment


@router.get("/{id}/comments/", response_model=list[CommentSchema])
async def get_comments_on_posts(id: int):
    """Read all Comments on a Post"""
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return [comment for comment in comment_table.values() if comment["post_id"] == id]


@router.get("/posts_and_comments/{id}/", response_model=PostWithCommentsSchema)
async def get_post_with_comments(id: int):
    """Read a Post with all its Comments"""
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = [
        comment for comment in comment_table.values() if comment["post_id"] == id
    ]
    return {"post": post, "comments": comments}
