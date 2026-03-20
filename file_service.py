#Exports data inputted from main to file

import json
import os
import csv
import shutil
from datetime import datetime
from config import USERS_FILE, EXPORT_FILE, BACKUP_FOLDER
from logging_service import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")
EXPORT_FILE = os.path.join(BASE_DIR, "exports", "users_export.csv")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backups")

def load_users():
    logger.info(f"Loading users from {USERS_FILE}")
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    logger.warning("users.json file was not found. Returning empty list.")
    return []

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)
    logger.info(f"Saved {len(users)} users to {USERS_FILE}")

def export_users_to_csv(users, pause):
    if not users:
        print("No users to export.")
        pause()
        return

    os.makedirs(os.path.dirname(EXPORT_FILE), exist_ok=True)

    with open(EXPORT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Color", "Game", "Country"])

        for u in users:
            writer.writerow([
                u["id"],
                u["name"],
                u["age"],
                u["color"],
                u["game"],
                u["country"]
            ])
    logger.info(f"Exported {len(users)} users to {EXPORT_FILE}")
    print(f"Users exported to {EXPORT_FILE}")
    pause()

def backup_users():
    if not os.path.exists(USERS_FILE):
        return

    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = os.path.join(BACKUP_FOLDER, f"backup_users_{timestamp}.json")

    shutil.copy(USERS_FILE, backup_name)
    logger.info(f"Created backup file: {backup_name}")
    print(f"Backup created: {backup_name}")