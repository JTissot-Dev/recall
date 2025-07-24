from sqlmodel import Session
from app.core.database import engine
from app.database.seeders.data import seed_conversations, seed_messages


def seed():
    with Session(engine) as session:
        session.add_all(seed_conversations)
        session.add_all(seed_messages)
        session.commit()
        print(
            f"{len(seed_conversations)} conversations et {len(seed_messages)} messages insérés."
        )


if __name__ == "__main__":
    seed()
