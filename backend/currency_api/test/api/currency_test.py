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
                "currency_group_id": 1,
                "num_code": 36,
                "char_code": "AUD",
                "name": "Australian dollar"
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "currency_group_id": 1,
                "num_code": 36,
                "char_code": "AUD",
                "name": "Australian dollar"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "currency_group_id": 1,
                "num_code": "string",
                "char_code": "AZN",
                "name": "Azerbaijani manat"
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_add_currency(
    client: AsyncClient,
    payload: dict, status_code: int
):
    response = await client.post("/currency/", json=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["char_code"] == response.json()["char_code"]


@pytest.mark.parametrize(
    "currency_id, params, status_code",
    (
        (
            None,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "include_currency_rates": 1,
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
async def test_get_currency(
    client: AsyncClient,
    currency_id: Optional[int], params: dict, status_code: int
):
    response = await client.get(f"/currency/{currency_id if currency_id else ''}", params=params)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "currency_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "name": "Not Australian dollar"
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
async def test_upd_currency(
    client: AsyncClient,
    currency_id: Optional[int], payload: dict, status_code: int
):
    response = await client.patch(f"/currency/{currency_id}", json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "currency_id, status_code",
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
async def test_delete_currency(
    client: AsyncClient,
    currency_id: Optional[int], status_code: int
):
    response = await client.delete(f"/currency/{currency_id}")
    assert response.status_code == status_code
