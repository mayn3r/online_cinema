from tortoise import fields

from .base import AbstractBaseModel, TimestampMixin
from .extra import Watchlist
from src.app.schemas.enums import RoleEnum


class UserAccount(AbstractBaseModel, TimestampMixin):
    """ Модель пользователя """
    watchlist: Watchlist
    
    email = fields.CharField(max_length=64, unique=True)
    password_hash = fields.CharField(max_length=512)
    name = fields.CharField(max_length=128)
    balance = fields.IntField(default=0)
    username = fields.CharField(max_length=32, unique=True)
    is_premium = fields.BooleanField(default=False)
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.USER)
    
    class Meta:
        table="users"