import json

import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    """Helper function to create a post"""
    response = await async_client.post(
        "/api/v1/posts/", content=json.dumps({"body": body})
    )
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    """Helper function to create a comment"""
    response = await async_client.post(
        "/api/v1/posts/comments/",
        content=json.dumps({"body": body, "post_id": post_id}),
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient) -> dict:
    """Fixture for a created post"""
    return await create_post("Test Post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict) -> dict:
    """Fixture for a created comment"""
    return await create_post("Test Comment", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"

    response = await async_client.post(
        "/api/v1/posts/",
        content=json.dumps({"body": body}),
    )

    assert response.status_code == 201
    assert {"id": 1, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_invalid_json(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/posts/",
        content=json.dumps({}),
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_read_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/api/v1/posts/")

    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test Comment"

    response = await async_client.post(
        "/api/v1/posts/comments/",
        content=json.dumps({"body": body, "post_id": created_post["id"]}),
    )

    assert response.status_code == 201
    assert {
        "id": 1,
        "body": body,
        "post_id": created_post["id"],
    }.items() <= response.json().items()
