from file_service import load_users
from database_service import init_db, create_user, get_user_by_name

def migrate():
    init_db()
    users = load_users()

    for user in users:
        existing = get_user_by_name(user["name"])
        if not existing:
            create_user(
                user["name"],
                user["age"],
                user["color"],
                user["game"],
                user["country"]
            )

    print("Migration complete.")

if __name__ == "__main__":
    migrate()