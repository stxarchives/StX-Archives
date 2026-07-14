import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL", "")
key = os.getenv("SUPABASE_KEY", "")

supabase = create_client(url, key)

new_experiences = [
    {
        "name": "Anonymous",
        "email": "",
        "category": "Facilities & Infrastructure",
        "date": "2026-07-13",
        "title": "Broken Infrastructure Everywhere",
        "details": "The school is falling apart. There are broken washrooms, broken windows in almost every single classroom, damaged benches, and the drinking water quality is extremely bad.",
        "is_verified": True,
        "is_anonymous": True
    },
    {
        "name": "Anonymous",
        "email": "",
        "category": "Policies & Rules",
        "date": "2026-07-12",
        "title": "Forced Religious Practices & Discrimination",
        "details": "The school administrators are forcing students to sing and dance to Christian songs, practically forcing a change of religion. Additionally, there is blatant religious discrimination regarding holidays; they give holidays for Muslim and Christian celebrations but deny them for Hindu celebrations, such as refusing to give a holiday on Hanuman Jayanti.",
        "is_verified": True,
        "is_anonymous": True
    },
    {
        "name": "Anonymous",
        "email": "",
        "category": "Fee Discrepancies",
        "date": "2026-07-11",
        "title": "Extortion for Farewell & Books",
        "details": "They collect farewell contributions from all students from Class 9 to Class 12, taking over ₹1500+ and increasing the price as the class level gets higher. Despite this massive collection, they then forced students to dance at the farewell themselves, and the food provided was of terrible quality. Why take so much money if the students have to do everything themselves? Furthermore, the required Physical Education book is still not available in the school.",
        "is_verified": True,
        "is_anonymous": True
    },
    {
        "name": "Anonymous",
        "email": "",
        "category": "Facilities & Infrastructure",
        "date": "2026-07-09",
        "title": "Unhealthy Canteen Food",
        "details": "Despite being a school that should promote health, the canteen itself sells unhealthy junk food to students.",
        "is_verified": True,
        "is_anonymous": True
    }
]

for exp in new_experiences:
    try:
        supabase.table('experiences').insert(exp).execute()
        print(f"Inserted: {exp['title']}")
    except Exception as e:
        print(f"Error inserting {exp['title']}: {e}")

print("Done!")
