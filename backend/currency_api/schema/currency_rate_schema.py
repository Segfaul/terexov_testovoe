from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.currency_api.util import _AllOptionalMeta


class CurrencyRateSchema(BaseModel):
    """
    Pydantic schema for CurrencyRate table data.

    Attributes:
    ----------
    - currency_id: identifier of the currency associated with the entry.
    - nominal: currency_rate nominal value.
    - value: currency_rate value with precision of 4.
    - vunit_rate: currency_rate vunit rate.
    """
    currency_id: int
    nominal: int
    value: float
    vunit_rate: float

    model_config = ConfigDict(from_attributes=True)


class PartialCurrencyRateSchema(CurrencyRateSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for CurrencyRate table data (PATCH).
    """


class IndependentCurrencyRateSchema(CurrencyRateSchema):
    """
    Pydantic schema for CurrencyRate table data (subqueries).

    Attributes:
    ----------
    - id: unique identifier of the currency rate.
    - currency_id: identifier of the currency associated with the entry.
    - nominal: currency_rate nominal value.
    - value: currency_rate value with precision of 4.
    - vunit_rate: currency_rate vunit rate.
    - modified_at: date the currency_rate was modified.
    """
    id: int
    modified_at: datetime


class CurrencyRateResponse(IndependentCurrencyRateSchema):
    """
    Pydantic schema for CurrencyRate table data.

    Attributes:
    ----------
    - id: unique identifier of the currency rate.
    - currency_id: identifier of the currency associated with the entry.
    - nominal: currency_rate nominal value.
    - value: currency_rate value with precision of 4.
    - vunit_rate: currency_rate vunit rate.
    - modified_at: date the currency_rate was modified.
    """
