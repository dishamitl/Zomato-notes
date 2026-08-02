from database import SessionLocal, engine
from models import Base, User, Note
from ranking_dataset import RANKING_DATASET
from ai_sample_notes import AI_SAMPLE_NOTES

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear database
db.query(Note).delete()
db.query(User).delete()
db.commit()

# ---------------- Users ----------------

SEED_USERS = [
    {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "password": "alicepass123"
    },
    {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
        "password": "bobpass123"
    }
]

# ---------------- Main Notes ----------------

SEED_NOTES = [
    {
        "id": 1,
        "owner_id": 1,
        "title": "Standup Summary",
        "tag": "work",
        "content": "Discussed sprint progress, blockers on the payments API integration, and the plan for the demo on Friday."
    },
    {
        "id": 2,
        "owner_id": 1,
        "title": "Sprint Retro Notes",
        "tag": "work",
        "content": "Retro highlighted communication gaps between frontend and backend teams and agreed on daily syncs."
    },
    {
        "id": 3,
        "owner_id": 2,
        "title": "One on One",
        "tag": "work",
        "content": "Quick check-in, discussed career goals for next quarter."
    },
    {
        "id": 4,
        "owner_id": 1,
        "title": "Morning Run",
        "tag": "health",
        "content": "Ran 5km before breakfast."
    },
    {
        "id": 5,
        "owner_id": 2,
        "title": "Doctor Visit",
        "tag": "health",
        "content": "Annual checkup completed successfully."
    },
    {
        "id": 6,
        "owner_id": 1,
        "title": "Pasta Recipe",
        "tag": "recipes",
        "content": "Boil pasta, add tomatoes, basil and garlic."
    },
    {
        "id": 7,
        "owner_id": 2,
        "title": "Smoothie Recipe",
        "tag": "recipes",
        "content": "Blend banana, spinach and almond milk."
    },
    {
        "id": 8,
        "owner_id": 1,
        "title": "Flight Booking",
        "tag": "travel",
        "content": "Booked December vacation flights."
    },
    {
        "id": 9,
        "owner_id": 2,
        "title": "Random Thought",
        "tag": "random",
        "content": "A recommendation engine would improve note discovery."
    },
    {
        "id": 10,
        "owner_id": 1,
        "title": "Quote To Remember",
        "tag": "random",
        "content": "Done is better than perfect."
    }
]

# ---------------- Insert Users ----------------

for user in SEED_USERS:
    db.add(User(**user))

db.commit()

# ---------------- Insert Notes ----------------

for note in SEED_NOTES:
    db.add(Note(**note))

db.commit()

# ---------------- Ranking Dataset ----------------

for note in RANKING_DATASET:
    db.add(
        Note(
            title=note["title"],
            content=note["content"],
            tag="kb-demo",
            owner_id=1
        )
    )

db.commit()

# ---------------- AI Sample Notes ----------------

for note in AI_SAMPLE_NOTES:
    db.add(
        Note(
            title=note["title"],
            content=note["content"],
            tag="ai-demo",
            owner_id=2
        )
    )

db.commit()

db.close()

print("Database seeded successfully!")