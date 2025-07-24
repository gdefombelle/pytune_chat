from uuid import UUID
from typing import Optional
import json

from redis.asyncio import Redis
from pytune_configuration.redis_config import get_redis_client
from pytune_data.models import User

from .models import Conversation, Message

REDIS_HISTORY_TTL = 3600  # Durée de vie du cache : 1 heure

async def create_conversation(user_id: int, topic: Optional[str] = None) -> Conversation:
    try:
        user = await User.get(id=user_id)
        return await Conversation.create(user=user, topic=topic)
    except Exception as e:
        print("❌ Error in create_conversation:", e)
        raise


async def append_message(conversation_id: UUID, role: str, content: str) -> Message:
    try:
        # 🔎 On récupère bien l'objet Conversation à partir de son UUID
        conversation = await Conversation.get(id=conversation_id)
        msg = await Message.create(conversation=conversation, role=role, content=content)
    except Exception as e:
        print(f"❌ Error in append_message (DB): {e}")
        raise

    try:
        # 🧠 Met à jour le cache Redis
        redis: Redis = await get_redis_client()
        key = f"chat_history:{conversation_id}"

        cached = await redis.get(key)
        history = json.loads(cached) if cached else []
        history.append({"role": role, "content": content})
        await redis.set(key, json.dumps(history), ex=REDIS_HISTORY_TTL)
    except Exception as e:
        print(f"⚠️ Redis update failed in append_message: {e}")

    return msg

async def get_conversation_history(conversation_id: UUID) -> list[dict]:
    redis: Redis = await get_redis_client()
    key = f"chat_history:{conversation_id}"

    cached = await redis.get(key)
    if cached:
        return json.loads(cached)

    # Sinon, on fallback en BDD
    messages = await Message.filter(conversation_id=conversation_id).order_by("created_at")
    result = [{"role": m.role, "content": m.content} for m in messages]

    # Cache la version reconstruite
    await redis.set(key, json.dumps(result), ex=REDIS_HISTORY_TTL)

    return result


async def list_user_conversations(user_id: int) -> list[Conversation]:
    return await Conversation.filter(user__id=user_id).order_by("-started_at")
