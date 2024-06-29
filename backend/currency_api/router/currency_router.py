from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.currency_api.service.db_service import get_session
from backend.currency_api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, process_query_params, cache
from backend.currency_api.model import Currency
from backend.currency_api.schema import CurrencySchema, PartialCurrencySchema, CurrencyResponse

router = APIRouter(
    prefix="/v1/currency",
    tags=['Currency']
)


@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[CurrencyResponse], response_model_exclude_unset=True
)
@cache(expire=300)
async def read_all_currencies(
    request: Request,
    include_currency_rates: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    query_params: dict = process_query_params(request)
    return [
        CurrencyResponse(**currency.__dict__).model_dump(exclude_unset=True)
        async for currency in Currency.read_all(
            db_session,
            **query_params
        )
    ]


@router.get(
    "/{currency_id}", status_code=status.HTTP_200_OK,
    response_model=CurrencyResponse, response_model_exclude_unset=True
)
@cache(expire=60)
async def read_currency(
    request: Request,
    currency_id: int = Path(...),
    include_currency_rates: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    currency = await get_object_or_raise_404(
        db_session, Currency, currency_id,
        include_currency_rates=include_currency_rates
    )
    return CurrencyResponse(**currency.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=CurrencyResponse, response_model_exclude_unset=True
)
async def create_currency(
    request: Request,
    payload: CurrencySchema,
    db_session: AsyncSession = Depends(get_session)
):
    currency = await create_object_or_raise_400(db_session, Currency, **payload.model_dump())
    return CurrencyResponse(**currency.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{currency_id}", status_code=status.HTTP_200_OK,
    response_model=CurrencyResponse, response_model_exclude_unset=True
)
async def update_currency(
    request: Request,
    payload: PartialCurrencySchema, currency_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    currency = await get_object_or_raise_404(db_session, Currency, currency_id)
    await update_object_or_raise_400(db_session, Currency, currency, **payload.model_dump())
    return CurrencyResponse(**currency.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{currency_id}", status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_currency(
    request: Request,
    currency_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    currency = await get_object_or_raise_404(db_session, Currency, currency_id)
    await Currency.delete(db_session, currency)
