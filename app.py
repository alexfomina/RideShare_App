from db import rideshare_ops

#global variable
db = rideshare_ops()

global username 
global password
global user_status 

def main_menu():
    print("Welcome to RideSHare!")
    user_input = input("Do you have an existing account? (Y/N)")
    if user_input == "Y":
        user_status = input("Are you a Rider or Driver? Enter (R/D)")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        status = db.check_user_account(user_status, username, password)
        if status == True:
            if user_status == "D":
                driver_menu()
            else:
                rider_menu()
        else:
            create_account
    else:
        create_account()

def create_account():
    user_status = input("Would you like to create a Rider or Driver account? Enter (R) or (D)")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    db.create_user_account(user_status, username, password)

def driver_menu():
#View Rating: This will show the driver their current rating. This will be the
#average rating of all rides they have given.
#b. View Rides: This will show the driver the list of all rides they have given.
#c. Activate/Deactivate Driver Mode: This updates a flag on their profile, letting
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
        print("Current rating is ...")
        db.get_rating(username, password)
    if user_choice == 2:
        db.get_rides(username, password)
    if user_choice == 3:
        db.change_driver_mode(username, password)
    elif user_choice == 4:
        print("Thank you!")
    else:
        return 0

def rider_menu():
    #user_status, username, password
#View Rides: This will show the rider the list of all rides they have taken
# b.Find a driver:
# Match the rider with a driver that has their driver mode activated
# i. The rider will then provide the following info:
#   1.Pick up location
#   2. Drop off location
# ii. You will then create a ride and record that the driver drove that rider to the locations specified.
# iii. # You will then send the rider back to their options menu
# c.Rate my driver:
# i. You will look up the rider’s most recent ride
# ii. You will then print the information of this ride to the user and ask if it is correct.
# iii. If it is not the correct ride, you will have them enter the rideID of the ride they want to rate. Print that ride’s information and have them confirm.
# iv # Store the rating the rider gave on the ride recor
    print("Hi!")
    user_choice = input('''
    WELCOME RIDER!
    SELECT FROM THE FOLLOWING MENU:
    1. View rides
    2. Find a rider
    3. Rate my driver
    4. Exit
    ''')
    if user_choice == 1:
        db.get_rides(username, password)
    elif user_choice == 2:
        pick_up_location = input("Please enter the pickup location:")
        drop_off_location = input("Please enter drop-off location:")
        db.find_rides(user_status, username, password, pick_up_location, drop_off_location)
    elif user_choice == 3:
        db.find_recent_ride(user_status, username, password)
        ride_input = input("Is this the correct ride information? (Y/N)")
        if ride_input == "N":
            rideID = input("Please enter the rideID")
            db.find_ride(rideID)
    elif user_choice == 4:
        print("Bye! \n")
    else:
        rider_menu()
