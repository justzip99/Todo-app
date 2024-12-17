from tortoise.models import Model
from tortoise.fields import (
    CharField,
    UUIDField,
    BooleanField,
    DatetimeField,
    ForeignKeyField
)


class Todo(Model):
    id = UUIDField(pk=True)
    title = CharField(max_length=150, null=False)
    done = BooleanField(default=False, null=False)
    created_at = DatetimeField(auto_now_add=True, null=False)
    user = ForeignKeyField("models.User", related_name="todos")

    class Meta:
        table = "todos"  # Table name
        ordering = ["created_at"]  # Order by created_at DESC
