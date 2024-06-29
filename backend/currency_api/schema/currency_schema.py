from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.currency_api.util import _AllOptionalMeta
from backend.currency_api.schema.currency_rate_schema import IndependentCurrencyRateSchema


class CurrencySchema(BaseModel):
    """
    Pydantic schema for Currency table data.

    Attributes:
    ----------
    - currency_group_id: identifier of the currency_group associated with the entry.
    - num_code: currency numeric code with precision of 3.
    - char_code: currency character code.
    - name: currency full title.
    """
    currency_group_id: int
    num_code: int
    char_code: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class PartialCurrencySchema(CurrencySchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for Currency table data (PATCH).
    """


class IndependentCurrencySchema(CurrencySchema):
    """
    Pydantic schema for Currency table data (subqueries).

    Attributes:
    ----------
    - id: unique identifier of the Currency.
    - currency_group_id: identifier of the currency_group associated with the entry.
    - num_code: currency numeric code with precision of 3.
    - char_code: currency character code.
    - name: currency full title.
    - created_at: date the currency was created.
    """
    id: int
    created_at: datetime


class CurrencyResponse(IndependentCurrencySchema):
    """
    Pydantic schema for Currency table data.

    Attributes:
    ----------
    - id: unique identifier of the Currency.
    - currency_group_id: identifier of the currency_group associated with the entry.
    - num_code: currency numeric code with precision of 3.
    - char_code: currency character code.
    - name: currency full title.
    - created_at: date the currency was created.
    - currency_rates: rates related to the currency.
    """
    currency_rates: Optional[List[IndependentCurrencyRateSchema]] = None
