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
                "currency_id": 1,
                "nominal": 1,
                "value": 56.7995,
                "vunit_rate": 56.7995
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "currency_id": 1,
                "nominal": 1,
                "value": 'string',
                "vunit_rate": 'string'
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_add_currency_rate(
    client: AsyncClient,
    payload: dict, status_code: int
):
    response = await client.post("/currency_rate/", json=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["vunit_rate"] == response.json()["vunit_rate"]


@pytest.mark.parametrize(
    "currency_rate_id, params, status_code",
    (
        (
            None,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "currency_id": 1,
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
async def test_get_currency_rate(
    client: AsyncClient,
    currency_rate_id: Optional[int], params: dict, status_code: int
):
    response = await client.get(
        f"/currency_rate/{currency_rate_id if currency_rate_id else ''}", params=params
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "currency_rate_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "value": 57.7995,
                "vunit_rate": 57.7995
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
async def test_upd_currency_rate(
    client: AsyncClient,
    currency_rate_id: Optional[int], payload: dict, status_code: int
):
    response = await client.patch(f"/currency_rate/{currency_rate_id}", json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "currency_rate_id, status_code",
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
async def test_delete_currency_rate(
    client: AsyncClient,
    currency_rate_id: Optional[int], status_code: int
):
    response = await client.delete(f"/currency_rate/{currency_rate_id}")
    assert response.status_code == status_code
