#User input part
from logging_service import logger

def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1

def get_user():
    while True:
        name = input("Enter name (or 'exit'): ").strip().lower()

        if name == "exit":
            return None
        
        if name == "":
            print("name cannot be empty.")
            continue
        break

    while True:
        try:
            age = int(input("Enter age: "))
            if age < 0:
                print("Age cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid Number! Try again.")

    color = input("Enter favorite color: ").strip().lower()
    game = input("Enter favorite game: ").strip().lower()
    country = input("Enter favorite country: ").strip().lower()

    return {
        "name": name,
        "age": age,
        "color": color,
        "game": game,
        "country": country    
    }
def add_user(users, pause):
    user = get_user()

    if not user:
        return
    
    if any(u["name"].lower() == user["name"].lower() for u in users):
        print("User already exists.")
        return
    
    user_id = get_next_id(users)

    user = {
        "id": user_id,
        "name": user["name"],
        "age": user["age"],
        "color": user["color"],
        "game": user["game"],
        "country": user["country"]
    }

    users.append(user)
    logger.info(f"Added user '{user['name']}' with ID {user['id']}")
    print("User added.")
    pause()

def get_status(age):
    if age >= 30:
        return "In their prime"
    else:
        return "Still young"

def view_users(users, pause):
    if not users:
        print("No users found.")
        pause()
        return
    
    for u in users:
        status = get_status(u["age"])
        print(f"ID:{u['id']} | {u['name']} ({status}) - {u['color']} - {u['game']} - {u['country']}")
    

    pause()

def search_user(users, pause):
    search = input("Enter name to search: ").lower()
    found = False

    for u in users:
        if search in u["name"].lower():
            print(f"Found: {u['name']} - {u['age']} - {u['color']} - {u['game']} - {u['country']}")
            found = True
    
    if not found:
        print("User not found.")
    
    pause()

def search_user_by_id(users, pause):
    try:
        search_id = int(input("Enter ID to search: "))
    except ValueError:
        print("Invalid ID.")
        pause()
        return
    
    for u in users:
        if u["id"] == search_id:
            print(f"Found: ID:{u['id']} | {u['name']} - {u['color']} - {u['game']} - {u['country']}")
            pause()
            return
    
    print("User not found.")
    pause()

def delete_user(users, pause):
    try:
        delete_id = int(input("Enter ID to delete: "))
    except ValueError:
        logger.warning("User attempted to delete with invalid ID input")
        print("Invalid ID.")
        pause()
        return
    
    for u in users:
        if u["id"] == delete_id:
            users.remove(u)
            print("User deleted.")
            pause()
            return
    
    logger.warning(f"Delete attempted for non-existent user ID {delete_id}")
    print("User not found.")
    pause()

def update_user(users, pause):
    try:
        user_id = int(input("Enter user ID to update: "))
    except ValueError:
        logger.warning("Invalid ID entered during update.")
        print("Invalid ID.")
        pause()
        return
    
    for u in users:
        if u["id"] == user_id:

            print("\nWhat do you want to update?")
            print("1. Name")
            print("2. Age")
            print("3. Color")
            print("4. Game")
            print("5. Country")

            choice = input("Choose option: ")

            if choice == "1":
                while True:
                    new_name = input("Enter new name: ").strip().lower()
                    if new_name == "":
                        print("name cannot be empty.")
                        continue
                    logger.info(f"User ID {user_id} name changed from {u['name']} to {new_name}")
                    u["name"] = new_name
                    break
            
            elif choice == "2":
                try:
                    new_age = int(input("Enter new age: "))
                    if new_age < 0:
                        print("Age cannot be negative.")
                        pause()
                        return
                    logger.info(f"User ID {user_id} age changed from {u['age']} to {new_age}")
                    u["age"] = new_age
                except ValueError:
                    logger.warning("Invalid age entered during update.")
                    print("Invalid age.")
                    pause()
                    return
            
            elif choice == "3":
                new_color = input("Enter new favorite color: ").strip().lower()
                logger.info(f"User ID {user_id} color changed from {u['color']} to {new_color}")
                u["color"] = new_color

            elif choice == "4":
                new_game = input("Enter new favorite game: ").strip().lower()
                logger.info(f"User ID {user_id} game changed from {u['game']} to {new_game}")
                u["game"] = new_game
            
            elif choice == "5":
                new_country = input("Enter new favorite country: ").strip().lower()
                logger.info(f"User ID {user_id} country changed from {u['country']} to {new_country}")
                u["country"] = new_country
            
            else:
                logger.warning("Invalid update option selected.")
                print("Invalid choice.")
                pause()
                return
            
            logger.info(f"User with ID {user_id} updated successfully.")
            print("User updated.")
            pause()
            return
    
    logger.warning(f"Update attempted for non-existent user ID {user_id}")
    print("User not found.")
    pause()

            
def sort_users(users, pause):
    print("\nSort users by:")
    print("1. Name")
    print("2. Age")

    choice = input("Choose option: ")

    if choice == "1":
        sorted_users = sorted(users, key=lambda u: u["name"])
    elif choice == "2":
        sorted_users = sorted(users, key=lambda u: u["age"])
    else:
        print("Invalid choice.")
        pause()
        return
    
    for user in sorted_users:
        print(f'ID:{user["id"]} | {user["name"]} - {user["age"]}')

    pause()

def user_stats(users, pause):
    if not users:
        print("No users in database.")
        pause()
        return
    
    total = len(users)
    ages = [u["age"] for u in users]
    ave_age = sum(ages) / len(ages)

    youngest_user = min(users, key=lambda u: u["age"])
    oldest_user = max(users, key=lambda u: u["age"])

    print("\n--- USER STATS ---")
    print(f"Total users: {total}")
    print(f"Average age: {ave_age:.1f}")
    print(f"Youngest age: {youngest_user['name']} ({youngest_user['age']})")
    print(f"Oldest age: {oldest_user['name']} ({oldest_user['age']})")

    pause()

def most_common(users, field, pause):
    if not users:
        print("No users in database.")
        pause()
        return
    
    counts = {}

    for u in users:
        value =u[field]

        if value in counts:
            counts[value] += 1
        else:
            counts[value] = 1
    
    most_common_value = max(counts, key=counts.get)

    print(f"\nMost popular {field}: {most_common_value} ({counts[most_common_value]} users)")
    pause ()

def popular_menus(users, pause):
    print("\nCheck most popular:")
    print("1. Game")
    print("2. Color")
    print("3. Country")

    choice = input("Choose option: ")

    if choice == "1":
        most_common(users, "game", pause)
    elif choice == "2":
        most_common(users, "color", pause)
    elif choice == "3":
        most_common(users, "country", pause)
    else:
        print("Invalid choice.")
        pause()
