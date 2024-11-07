from db import rideshare_ops

#global variable
db = rideshare_ops()

def main_menu():
    print("Welcome to RideSHare!")
    user_input = input("Do you have an existing account? (Y/N)")
    if user_input == "Y":
        user_status = input("Are you a Rider or Driver? Enter (R/D)")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        db.check_user_account(user_status, username, password)
    else:
        create_account()

def create_account():
    user_status = input("Would you like to create a Rider or Driver account? Enter (R) or (D)")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    db.create_new_account(user_status, username, password)

def driver_menu():
#View Rating: This will show the driver their current rating. This will be the
#average rating of all rides they have given.
#b.
#View Rides: This
#will show the driver the list of all rides they have given.
#c.
#Activate/Deactivate Driver Mode: This updates a flag on their profile, letting
#riders know if they are accepting new rides right no
    user_choice = input('''
    WELCOME DRIVER!
    SELECT FROM THE FOLLOWING MENU:
    1. View your rating
    2. View Rides
    3. Activate/Deactivate Driver Mode
    4. Exit
    ''')
    if user_choice == '1':
        #get_rating should return 
        printf("Current rating is ...") + db.get_rating()
    elif user_choice == '4':
        printf("Thank you!")
    else:
        return 0
    

def main():
   # db.create_tables()  #only run once
    main_menu()
    db.close_connection()

if __name__ == '__main__':
    main()