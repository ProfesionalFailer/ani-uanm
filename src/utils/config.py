import os
from dotenv import load_dotenv

load_dotenv()

ANIMEUNITY_URL = os.getenv("ANIMEUNITY_URL")

if not ANIMEUNITY_URL:
    raise RuntimeError("Missing ANIMEUNITY_URL")

REDIRECT_PORT = os.getenv("REDIRECT_PORT")

if not REDIRECT_PORT:
    raise RuntimeError("Missing REDIRECT_PORT")
if not REDIRECT_PORT.isdigit():
    raise ValueError(f"{REDIRECT_PORT} is not a valid port")

REDIRECT_PORT = int(REDIRECT_PORT)
if REDIRECT_PORT > 65535 or REDIRECT_PORT < 0:
    raise OverflowError("bind(): port must be 0-65535")
