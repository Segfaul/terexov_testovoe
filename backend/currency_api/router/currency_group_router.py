from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.currency_api.service.db_service import get_session
from backend.currency_api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, process_query_params, cache
from backend.currency_api.model import CurrencyGroup
from backend.currency_api.schema import CurrencyGroupSchema, PartialCurrencyGroupSchema, \
    CurrencyGroupResponse

router = APIRouter(
    prefix="/v1/currency_group",
    tags=['CurrencyGroup']
)


@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[CurrencyGroupResponse], response_model_exclude_unset=True
)
@cache(expire=300)
async def read_all_currency_groups(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    query_params: dict = process_query_params(request)
    return [
        CurrencyGroupResponse(**currency_group.__dict__).model_dump(exclude_unset=True)
        async for currency_group in CurrencyGroup.read_all(
            db_session,
            **query_params
        )
    ]


@router.get(
    "/{currency_group_id}", status_code=status.HTTP_200_OK,
    response_model=CurrencyGroupResponse, response_model_exclude_unset=True
)
@cache(expire=60)
async def read_currency_group(
    request: Request,
    currency_group_id: int = Path(...),
    include_currencies: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    currency_group = await get_object_or_raise_404(
        db_session, CurrencyGroup, currency_group_id,
        include_currencies=include_currencies
    )
    return CurrencyGroupResponse(**currency_group.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=CurrencyGroupResponse, response_model_exclude_unset=True
)
async def create_currency_group(
    request: Request,
    payload: CurrencyGroupSchema,
    db_session: AsyncSession = Depends(get_session)
):
    currency_group = await create_object_or_raise_400(
        db_session, CurrencyGroup, **payload.model_dump()
    )
    return CurrencyGroupResponse(**currency_group.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{currency_group_id}", status_code=status.HTTP_200_OK,
    response_model=CurrencyGroupResponse, response_model_exclude_unset=True
)
async def update_currency_group(
    request: Request,
    payload: PartialCurrencyGroupSchema, currency_group_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    currency_group = await get_object_or_raise_404(
        db_session, CurrencyGroup, currency_group_id
    )
    await update_object_or_raise_400(
        db_session, CurrencyGroup, currency_group, **payload.model_dump()
    )
    return CurrencyGroupResponse(**currency_group.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{currency_group_id}", status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_currency_group(
    request: Request,
    currency_group_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    currency_group = await get_object_or_raise_404(db_session, CurrencyGroup, currency_group_id)
    await CurrencyGroup.delete(db_session, currency_group)
