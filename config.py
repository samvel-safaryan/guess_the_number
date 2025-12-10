import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: str | None = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN is missing in .env")
