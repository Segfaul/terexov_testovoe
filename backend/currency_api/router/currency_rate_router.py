from typing import List

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.currency_api.service.db_service import get_session
from backend.currency_api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, process_query_params, cache
from backend.currency_api.model import CurrencyRate
from backend.currency_api.schema import CurrencyRateSchema, PartialCurrencyRateSchema, \
    CurrencyRateResponse

router = APIRouter(
    prefix="/v1/currency_rate",
    tags=['CurrencyRate']
)


@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[CurrencyRateResponse], response_model_exclude_unset=True
)
@cache(expire=300)
async def read_all_currency_rates(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    query_params: dict = process_query_params(request)
    return [
        CurrencyRateResponse(**currency_rate.__dict__).model_dump(exclude_unset=True)
        async for currency_rate in CurrencyRate.read_all(
            db_session,
            **query_params
        )
    ]


@router.get(
    "/{currency_rate_id}", status_code=status.HTTP_200_OK,
    response_model=CurrencyRateResponse, response_model_exclude_unset=True
)
@cache(expire=60)
async def read_currency_rate(
    request: Request,
    currency_rate_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    currency_rate = await get_object_or_raise_404(
        db_session, CurrencyRate, currency_rate_id
    )
    return CurrencyRateResponse(**currency_rate.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=CurrencyRateResponse, response_model_exclude_unset=True
)
async def create_currency_rate(
    request: Request,
    payload: CurrencyRateSchema,
    db_session: AsyncSession = Depends(get_session)
):
    currency_rate = await create_object_or_raise_400(
        db_session, CurrencyRate, **payload.model_dump()
    )
    return CurrencyRateResponse(**currency_rate.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{currency_rate_id}", status_code=status.HTTP_200_OK,
    response_model=CurrencyRateResponse, response_model_exclude_unset=True
)
async def update_currency_rate(
    request: Request,
    payload: PartialCurrencyRateSchema, currency_rate_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    currency_rate = await get_object_or_raise_404(
        db_session, CurrencyRate, currency_rate_id
    )
    await update_object_or_raise_400(
        db_session, CurrencyRate, currency_rate, **payload.model_dump()
    )
    return CurrencyRateResponse(**currency_rate.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{currency_rate_id}", status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_currency_rate(
    request: Request,
    currency_rate_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    currency_rate = await get_object_or_raise_404(db_session, CurrencyRate, currency_rate_id)
    await CurrencyRate.delete(db_session, currency_rate)
