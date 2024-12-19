from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str]
    age: Mapped[int]

    __table_args__ = UniqueConstraint('full_name', 'age'),
