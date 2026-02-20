import os
from dotenv import load_dotenv

load_dotenv()

ANIMEUNITY_URL = os.getenv("ANIMEUNITY_URL")

if not ANIMEUNITY_URL:
    raise RuntimeError("Missing ANIMEUNITY_URL")
