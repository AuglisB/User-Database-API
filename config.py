#Nervous system(pathway)

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.join(BASE_DIR, "data")
EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backups")

USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
ADMINS_FILE = os.path.join(DATA_FOLDER, "admins.json")
EXPORT_FILE = os.path.join(EXPORT_FOLDER, "users_export.csv")
DB_FILE = os.path.join(DATA_FOLDER, "users.db")

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY is not set in environemnt variables")

JWT_SECRET = os.getenv("JWT_SECRET")

if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables")

if not JWT_SECRET:
    raise ValueError("JWT_SECRET is not set in environemnt variables")
