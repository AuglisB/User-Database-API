#Main app (start here)

import os
from auth_service import admin_login
from file_service import load_users, save_users, export_users_to_csv, backup_users
from user_service import (
    add_user,
    view_users,
    search_user,
    search_user_by_id,
    delete_user,
    update_user,
    sort_users,
    user_stats,
    popular_menus
)

#Functions 
#-------------------------------------------------------------------

def pause():
    input("\nPress Enter to continue...")

#-------------------------------------------------------------------------------

#Variable 
users = load_users()
current_admin = None
#Menu Loop
while True:
    print("\n======== USER DATABASE ========")
    print("1. Add user")
    print("2. View users")
    print("3. Search user by name")
    print("4. Search user by ID")
    print("5. Login")
    print("6. Delete user")
    print("7. Update user")
    print("8. Sort users")
    print("9. User statistics")
    print("10. Most popular stats")
    print("11. Export users to CSV")
    print("12. Logout")
    print("13. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_user(users, pause)
#---------------------------------------------------------------
    
    elif choice == "2":
        view_users(users, pause)
        
#------------------------------------------------------------------

    elif choice == "3":
        search_user(users, pause)

#--------------------------------------------------------------------
    
    elif choice == "4":
        search_user_by_id(users, pause)

#---------------------------------------------------------------------

    elif choice == "5":
        if current_admin:
            print(f"Already logged in as {current_admin['username']}.")
            pause()
        else:
            current_admin = admin_login()

#---------------------------------------------------------------------

    elif choice == "6":
        if current_admin and current_admin["role"] == "admin":
            delete_user(users, pause)
        else:
            print("Admin login required.")
            pause()

#--------------------------------------------------------------------   
    
    elif choice == "7":
        if current_admin and current_admin["role"] == "admin":
            update_user(users, pause)
        else:
            print("Admin login required.")
            pause()

#-------------------------------------------------------------------

    elif choice == "8":
        if current_admin and current_admin["role"] == "admin":
            sort_users(users, pause)
        else:
            print("Admin login required.")
            pause()

#-------------------------------------------------------------------

    elif choice == "9":
        if current_admin and current_admin["role"] == "admin":
            user_stats(users, pause)
        else:
            print("Admin login required.")
            pause()

#------------------------------------------------------------------

    elif choice == "10":
        if current_admin and current_admin["role"] == "admin":
            popular_menus(users, pause)
        else:
            print("Admin login required.")
            pause()
#---------------------------------------------------------------------

    elif choice == "11":
        if current_admin and current_admin["role"] == "admin":
            export_users_to_csv(users, pause)
        else:
            print("Admin login required.")
            pause()

#----------------------------------------------------------------------

    elif choice == "12":
        if current_admin:
            print(f"{current_admin['username']} has been logged out.")
            current_admin = None
        else:
            print("No admin is currently logged in.")
        pause()

#----------------------------------------------------------------------

    elif choice == "13":
        break

#Send dictionaries to a json file 
print("Saving file now...")
save_users(users)
backup_users()
print("File saved!")

# Shows exactly where the json is located
print("Saved to:", os.getcwd())
