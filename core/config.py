import os

from dotenv import load_dotenv

load_dotenv()

BOT_API_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "cab.db")
