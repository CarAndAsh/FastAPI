from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin



class Post(Base, UserRelationMixin):
    _user_back_populates = 'post'
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default='', server_default='')
