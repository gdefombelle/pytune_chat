# pytune_chat
# 🧠 pytune_chat

**pytune_chat** is the official conversation and dialogue orchestration package for the PyTune and EigenAgentUX projects.  
It provides persistent chat history management (PostgreSQL), caching (Redis), and optional embedding retrieval (Qdrant) to support long-form, multi-turn AI interactions.

---

## 📦 Features

- ✅ Persistent conversations per user (`Conversation`)
- ✅ Fine-grained message tracking (`Message`) with role (user, assistant, system)
- ✅ Async ORM support with Tortoise
- ✅ Helper functions: create, append, retrieve
- ✅ Designed to integrate with Redis (for session cache) and Qdrant (for RAG)
- ✅ Clean modular design for future AI orchestration logic

---

## 📁 Structure

pytune_chat/
├── init.py
├── models.py # ORM definitions
├── store.py # create_conversation, append_message, get_history, list_user_conversations

yaml
Copier
Modifier

---

## 🐢 Tortoise ORM Setup

Add this to your FastAPI init or Tortoise config:

```python
TORTOISE_ORM = {
    "connections": {"default": "postgres://user:password@localhost:5432/yourdb"},
    "apps": {
        "models": {
            "models": ["pytune_chat.models"],
            "default_connection": "default",
        },
    },
}
🚀 Usage
python
Copier
Modifier
from pytune_chat.store import create_conversation, append_message, get_conversation_history

conversation = await create_conversation(user_id=uuid4(), topic="Diagnose Steinway B11")
await append_message(conversation.id, "user", "Parle-moi du Steinway B11.")
await append_message(conversation.id, "assistant", "Le Steinway B11 est un quart de queue exceptionnel...")

history = await get_conversation_history(conversation.id)
🔧 Install
bash
Copier
Modifier
poetry add pytune_chat
If cloned locally:

bash
Copier
Modifier
cd pytune_chat
poetry install
📘 Roadmap
chat_orchestrator.py (LLM+RAG)

Redis integration

Token usage tracking

Slot filling / memory extraction

FastAPI Router exposure

🔗 License
MIT – Gabriel (PyTune / Eigen Vertex)