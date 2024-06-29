from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.currency_api.config import MOSCOW_TZ
from backend.currency_api.model.base import Base
from backend.currency_api.model.mixin import CRUDMixin
from backend.currency_api.model.currency_group import CurrencyGroup

if TYPE_CHECKING:
    from backend.currency_api.model.currency_rate import CurrencyRate
else:
    CurrencyRate = "CurrencyRate"


class Currency(Base, CRUDMixin):
    '''
    Currency instance

    Attributes
    ----------
    currency_group_id: int
        id of the currency_group associated with the record
    num_code: int
        currency numeric code with precision of 3
    char_code: str
        currency character code
    name: str
        currency full title
    created_at: datetime
        date the currency was created
    '''
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    currency_group_id: Mapped[int] = mapped_column(
        "currency_group_id", ForeignKey('currency_group.id'), nullable=False
    )
    num_code: Mapped[int] = mapped_column(
        "num_code", Numeric(precision=3, scale=0), nullable=False, unique=True
    )
    char_code: Mapped[str] = mapped_column(
        "char_code", String(length=3), nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        "name", String(length=64), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime(timezone=True),
        default=lambda: datetime.now(MOSCOW_TZ)
    )

    currency_group: Mapped[CurrencyGroup] = relationship(
        'CurrencyGroup', back_populates='currencies'
    )
    currency_rates: Mapped[List[CurrencyRate]] = relationship(
        'CurrencyRate', cascade='all, delete-orphan', back_populates='currency'
    )
