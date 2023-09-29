from pydantic import BaseModel


class CreatePostSchema(BaseModel):
    body: str


class PostSchema(CreatePostSchema):
    id: int


class CreateCommentSchema(BaseModel):
    body: str
    post_id: int


class CommentSchema(CreateCommentSchema):
    id: int


class PostWithCommentsSchema(BaseModel):
    post: PostSchema
    comments: list[CommentSchema]
