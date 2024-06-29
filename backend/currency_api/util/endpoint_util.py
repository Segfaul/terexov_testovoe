import json
from typing import Dict, Callable
from functools import wraps

from fastapi import Request, status, HTTPException
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_object_or_raise_404(db_session: AsyncSession, item, item_id: int, *args, **kwargs):
    """
    Response pattern for api endpoint if current item doesn't exist
    """
    instance = await item.read_by_id(db_session, item_id, *args, **kwargs)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item.__name__} not found"
        )
    return instance


async def create_object_or_raise_400(db_session: AsyncSession, item, **kwargs):
    """
    Response pattern for api endpoint if inegrity error occured (FK)
    """
    try:
        instance = await item.create(db_session, **kwargs)
        return instance
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"[{item.__name__}] Foreign key constraint violated: " + str(e.__cause__)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"[{item.__name__}] Internal server error: " + str(e.__cause__)
        ) from e


async def update_object_or_raise_400(db_session: AsyncSession, item, item_instance, **kwargs):
    """
    Response pattern for api endpoint if validator throws an error
    """
    try:
        await item.update(db_session, item_instance, **kwargs)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"[{item.__name__}] Foreign key constraint violated: " + str(e.__cause__)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"[{item.__name__}] Internal server error: " + str(e.__cause__)
        ) from e


def process_query_params(request: Request) -> Dict[str, str]:
    """
    Process query parameters from a FastAPI Request object
    """
    query_params = dict(request.query_params)
    limit_q = query_params.get('limit', None)
    offset_q = query_params.get('offset', None)
    query_params['limit'] = min(int(limit_q), 500) if str(limit_q).isdigit() else 500
    query_params['offset'] = offset_q if str(offset_q).isdigit() else 0

    return query_params


def cache(expire: int = 60) -> Callable:
    """
    Decorator for caching the result of an async function with an optional expiration time.

    :param expire : expiration time for the cache in seconds (default=60)
    :type expire : int
    :returns : function decorator
    :rtype : Callable

    Example:

    ```
        @cache(expire=300)
        async def fetch_data(request: Request, *args, **kwargs) -> dict:
            ...
            return data_dict
    ```
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            redis: Redis = request.app.state.redis
            query_params: dict = process_query_params(request)
            cache_key = f"{request.url.path}?" \
                f"{'&'.join([f'{key}={value}' for key, value in query_params.items()])}"
            cached_result = await redis.get(cache_key)

            if cached_result is None:
                result = await func(*args, request, **kwargs)
                await redis.set(cache_key, json.dumps(result, default=str), ex=expire)
                return result

            return json.loads(cached_result)

        return wrapper

    return decorator
