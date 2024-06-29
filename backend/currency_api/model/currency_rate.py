from datetime import datetime

from sqlalchemy import Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.currency_api.config import MOSCOW_TZ
from backend.currency_api.model.base import Base
from backend.currency_api.model.mixin import CRUDMixin
from backend.currency_api.model.currency import Currency


class CurrencyRate(Base, CRUDMixin):
    '''
    Currency instance

    Attributes
    ----------
    currency_id: int
        id of the currency associated with the record
    nominal: int
        currency nominal value
    value: float
        currency value with precision of 4
    vunit_rate: float
        currency vunit rate
    modified_at: datetime
        date the currency_rate was modified
    '''
    __tablename__ = "currency_rate"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    currency_id: Mapped[int] = mapped_column(
        "currency_id", ForeignKey('currency.id'), nullable=False
    )
    nominal: Mapped[int] = mapped_column(
        "nominal", Integer, default=1, nullable=False
    )
    value: Mapped[Float] = mapped_column(
        "value", Float(precision=4), nullable=False
    )
    vunit_rate: Mapped[Float] = mapped_column(
        "vunit_rate", Float, nullable=False
    )
    modified_at: Mapped[DateTime] = mapped_column(
        "modified_at", DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(MOSCOW_TZ),
        onupdate=lambda: datetime.now(MOSCOW_TZ)
    )

    currency: Mapped[Currency] = relationship('Currency', back_populates='currency_rates')
