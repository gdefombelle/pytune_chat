from uuid import uuid4
from tortoise import fields
from tortoise.models import Model
from enum import Enum

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Conversation(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    user = fields.ForeignKeyField("models.User", related_name="conversations")  # ✅

    topic = fields.TextField(null=True)
    started_at = fields.DatetimeField(auto_now_add=True)

    messages: fields.ReverseRelation["Message"]

    class Meta:
        table = "conversations"
        ordering = ["-started_at"]


class Message(Model):
    id = fields.IntField(pk=True)
    conversation = fields.ForeignKeyField("models.Conversation", related_name="messages", on_delete=fields.CASCADE)
    role = fields.CharField(max_length=16)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "messages"
        ordering = ["created_at"]
