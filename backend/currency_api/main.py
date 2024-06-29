import time
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from backend.currency_api.config import ALLOWED_ORIGINS
from backend.currency_api.router import currency_router, currency_rate_router, currency_group_router
from backend.currency_api.service.redis_service import get_redis

tags_metadata = [
    {
        "name": "CurrencyGroup",
        "description": "Currency group endpoint",
    },
    {
        "name": "Currency",
        "description": "Currency endpoint",
    },
    {
        "name": "CurrencyRate",
        "description": "Currency rate endpoint",
    },
]


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    '''
    Asynchronous context manager to manage the lifespan of a FastAPI application's Redis connection.
    '''
    app_instance.state.redis = await get_redis()
    try:
        yield
    finally:
        await app_instance.state.redis.close()


app = FastAPI(
    title="Currency Public API",
    summary="Chilled api service for parsing currencies 🐍",
    version='0.0.1',
    contact={
        "name": "Segfaul",
        "url": "https://github.com/segfaul",
    },
    openapi_url='/api/openapi.json',
    openapi_tags=tags_metadata,
    docs_url=None, redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(currency_router, prefix="/api")
app.include_router(currency_rate_router, prefix="/api")
app.include_router(currency_group_router, prefix="/api")


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    """
    TIMEOUT Middleware, throws an error if request exceeds 5s
    """
    start_time = time.time()
    try:
        return await asyncio.wait_for(call_next(request), timeout=5)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse(
            {
                'detail': 'Request processing time excedeed limit',
                'processing_time': process_time
            },
            status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )


@app.get("/api/swagger", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json", title="CurrencyAPI",
    )


@app.get("/api/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/api/openapi.json", title="CurrencyAPI",
    )
