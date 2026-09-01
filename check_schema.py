import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL", "")
key = os.getenv("SUPABASE_KEY", "")

supabase = create_client(url, key)

try:
    response = supabase.table('experiences').select('*').limit(1).execute()
    print("Columns:", response.data[0].keys() if response.data else "No data")
except Exception as e:
    print(f"Error: {e}")
