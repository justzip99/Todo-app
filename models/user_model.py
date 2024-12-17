from tortoise.models import Model
from tortoise.fields import CharField, DatetimeField, IntField, TextField


class User(Model):
    id = IntField(pk=True)
    email = CharField(max_length=150, null=False, unique=True)
    first_name = CharField(max_length=150, null=False)
    last_name = CharField(max_length=150, null=False)
    password_hash = CharField(max_length=150, null=False)
    refresh_token = TextField(null=True)


class Meta:
    table = "users"  # Table name
