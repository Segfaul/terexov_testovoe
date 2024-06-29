from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.currency_api.util import _AllOptionalMeta
from backend.currency_api.schema.currency_schema import IndependentCurrencySchema


class CurrencyGroupSchema(BaseModel):
    """
    Pydantic schema for CurrencyGroup table data.

    Attributes:
    ----------
    - name: name of the currency group.
    """
    name: str

    model_config = ConfigDict(from_attributes=True)


class PartialCurrencyGroupSchema(CurrencyGroupSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for CurrencyGroup table data (PATCH).
    """


class IndependentCurrencyGroupSchema(CurrencyGroupSchema):
    """
    Pydantic schema for CurrencyGroup table data (subqueries).

    Attributes:
    ----------
    - id: unique identifier of the currency group.
    - name: name of the currency group.
    - created_at: date the currency group was created.
    """
    id: int
    created_at: datetime


class CurrencyGroupResponse(IndependentCurrencyGroupSchema):
    """
    Pydantic schema for CurrencyGroup table data.

    Attributes:
    ----------
    - id: unique identifier of the currency group.
    - name: name of the currency group.
    - created_at: date the currency group was created.
    - currencies: currencies related to the group.
    """
    currencies: Optional[List[IndependentCurrencySchema]] = None
