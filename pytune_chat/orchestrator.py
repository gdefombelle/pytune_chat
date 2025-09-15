# pytune_chat/orchestrator.py

from pytune_chat.store import get_conversation_history, append_message
from pytune_llm.llm_client import ask_llm
from uuid import UUID


async def run_chat_turn(conversation_id: UUID, user_input: str, model: str = "gpt-4") -> str:
    # 1. Récupère l’historique
    history = await get_conversation_history(conversation_id)

    # 2. Formate les messages pour l'API OpenAI
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    messages.append({"role": "user", "content": user_input})

    # 3. Appelle le LLM
    from pytune_llm.llm_backends.openai_backend import call_openai_llm
    response_text = await call_openai_llm(
        messages=messages,
        model=model
    )

    # 4. Sauvegarde la question + réponse
    await append_message(conversation_id, "user", user_input)
    await append_message(conversation_id, "assistant", response_text)

    # 5. Retourne la réponse
    return response_text
