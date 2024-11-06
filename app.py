from db import db_operations

def main_menu():
    print("Welcome to RideSHare!")
    user_input = input("Do you have an existing account? (Y/N)")
    if user_input == "Y":
        db.login()
    else:
        create_account()

def create_account():
    choice = input("Would you like to create a Rider or Driver account? Enter (R) or (D)")
    if choice == "R":
        db.create_rider_account()
    elif choice == "D":
        db.create_driver_account()
    else:
        create_account()
