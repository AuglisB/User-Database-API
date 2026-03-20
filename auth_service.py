import json
import os
import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from config import ADMINS_FILE, JWT_SECRET

print("Auth service file loaded")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_admins():
    print("Looking for admins file at:", ADMINS_FILE)

    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: admins.json is empty or invalid.")
            input("\nPress Enter to continue...")
            return []
    return []


def authenticate_admin(username, password):
    admins = load_admins()
    hashed_password = hash_password(password)

    for admin in admins:
        if admin["username"] == username and admin["password"] == hashed_password:
            return admin

    return None


def create_token(admin):
    payload = {
        "username": admin["username"],
        "role": admin["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def admin_login():
    print("\n--- Admin Login ---")

    admins = load_admins()
    print("Loaded admins:", admins)
    attempts = 3

    while attempts > 0:
        username = input("Username: ")
        password = input("Password: ")

        hashed_password = hash_password(password)

        for admin in admins:
            if admin["username"] == username and admin["password"] == hashed_password:
                print("Login successful")
                return admin

        attempts -= 1
        print(f"Access denied. Attempts left: {attempts}")

    print("Too many failed login attempts.")
    input("\nPress Enter to continue...")
    return None