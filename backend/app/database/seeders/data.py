from uuid import uuid4
from datetime import datetime, timedelta, timezone
from app.models import Conversation, Message, Role

conversation_1_id = uuid4()
conversation_2_id = uuid4()

seed_conversations = [
    Conversation(
        id=conversation_1_id,
        title="Assistance technique",
        created_at=datetime.now(timezone.utc) - timedelta(days=1),
        updated_at=datetime.now(timezone.utc),
    ),
    Conversation(
        id=conversation_2_id,
        title="Questions sur le produit",
    ),
]

seed_messages = [
    Message(
        conversation_id=conversation_1_id,
        role=Role.user,
        content="Bonjour, j'ai un problème avec mon compte.",
        created_at=datetime.now(timezone.utc) - timedelta(days=1, minutes=10),
    ),
    Message(
        conversation_id=conversation_1_id,
        role=Role.assistant,
        content="Bonjour ! Pouvez-vous me donner plus de détails ?",
        created_at=datetime.now(timezone.utc) - timedelta(days=1, minutes=9),
    ),
    Message(
        conversation_id=conversation_2_id,
        role=Role.user,
        content="Le modèle GPT peut-il traiter des PDF ?",
    ),
    Message(
        conversation_id=conversation_2_id,
        role=Role.assistant,
        content="Oui, avec un traitement adapté du contenu du PDF en texte.",
    ),
]
