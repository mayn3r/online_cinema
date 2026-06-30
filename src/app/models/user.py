from tortoise import fields

from .base import AbstractBaseModel, TimestampMixin
from src.app.schemas.enums import RoleEnum


class UserAccount(AbstractBaseModel, TimestampMixin):
    """ Модель пользователя """
    email = fields.CharField(max_length=64)
    password_hash = fields.CharField(max_length=512)
    
    name = fields.CharField(max_length=128)
    balance = fields.IntField(default=0)
    username = fields.CharField(max_length=32)
    is_premium = fields.BooleanField(default=False)
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.USER)
    
    class Meta:
        table="users"