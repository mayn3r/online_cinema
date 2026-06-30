from tortoise import fields

from .base import AbstractBaseModel, TimestampMixin


class UserAccount(AbstractBaseModel, TimestampMixin):
    """ Модель пользователя """
    email = fields.CharField(max_length=64)
    password_hash = fields.CharField(max_length=512)
    
    name = fields.CharField(max_length=128)
    username = fields.CharField(max_length=32)
    is_premium = fields.BooleanField(default=False)
    
    class Meta:
        table="users"