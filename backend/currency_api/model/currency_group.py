from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.currency_api.config import MOSCOW_TZ
from backend.currency_api.model.base import Base
from backend.currency_api.model.mixin import CRUDMixin

if TYPE_CHECKING:
    from backend.currency_api.model.currency import Currency
else:
    Currency = "Currency"


class CurrencyGroup(Base, CRUDMixin):
    '''
    Currency Group instance

    Attributes
    ----------
    name: str
        currency group name
    created_at: datetime
        date the currency group was created
    '''
    __tablename__ = "currency_group"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        "name", String(length=128), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime(timezone=True),
        default=lambda: datetime.now(MOSCOW_TZ)
    )

    currencies: Mapped[List[Currency]] = relationship(
        'Currency', cascade='all, delete-orphan', back_populates='currency_group'
    )
