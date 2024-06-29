from typing import Optional

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {
                "name": "Foreign Currency Market"
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "name": 123
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_add_currency_group(
    client: AsyncClient,
    payload: dict, status_code: int
):
    response = await client.post("/currency_group/", json=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["name"] == response.json()["name"]


@pytest.mark.parametrize(
    "currency_group_id, params, status_code",
    (
        (
            None,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "include_currencies": 1,
            },
            status.HTTP_200_OK,
        ),
        (
            2,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
    ),
)
async def test_get_currency_group(
    client: AsyncClient,
    currency_group_id: Optional[int], params: dict, status_code: int
):
    response = await client.get(
        f"/currency_group/{currency_group_id if currency_group_id else ''}", params=params
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "currency_group_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "name": "Not Foreign Currency Market"
            },
            status.HTTP_200_OK,
        ),
        (
            2,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
    ),
)
async def test_upd_currency_group(
    client: AsyncClient,
    currency_group_id: Optional[int], payload: dict, status_code: int
):
    response = await client.patch(f"/currency_group/{currency_group_id}", json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "currency_group_id, status_code",
    (
        (
            1,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            2,
            status.HTTP_404_NOT_FOUND,
        )
    ),
)
async def test_delete_currency_group(
    client: AsyncClient,
    currency_group_id: Optional[int], status_code: int
):
    response = await client.delete(f"/currency_group/{currency_group_id}")
    assert response.status_code == status_code
