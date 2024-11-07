from datetime import datetime
import uuid
import mysql.connector

class rideshare_ops():

    def __init__(self):
        self.connection = mysql.connector.connect(host = 'localhost',
                                                user = 'root',
                                                password = 'HenryCPSC408!',
                                                auth_plugin = 'mysql_native_password',
                                                database = 'RideShare')
        #Cursor object to interact with database
        self.cursor = self.connection.cursor()

        print("Connection made")

    def create_tables(self):
        #create driver table
        query = '''
        CREATE TABLE DRIVER(
        driver_ID INT PRIMARY KEY NOT NULL,
        username VARCHAR(30) UNIQUE NOT NULL,
        password VARCHAR(30) NOT NULL,
        average_rating INT,
        driving_status BOOL DEFAULT False,
        name VARCHAR(30) NOT NULL
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print("Created driver table")

    
        #create rider table
        query = '''
        CREATE TABLE RIDER(
        rider_ID INT PRIMARY KEY NOT NULL,
        username VARCHAR(30) UNIQUE NOT NULL,
        password VARCHAR(30) NOT NULL,
        name VARCHAR(30) NOT NULL
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print("Created rider table")

        #create ride table
        query = '''
        CREATE TABLE RIDE(
        ride_ID INT PRIMARY KEY NOT NULL,
        rating INT,
        pickup_location VARCHAR(60),
        drop_off_location VARCHAR(60),
        time_stamp TIMESTAMP,
        driver_id INT,
        rider_id INT,
        FOREIGN KEY (driver_ID) REFERENCES DRIVER(driver_ID),
        FOREIGN KEY (rider_ID) REFERENCES RIDER(rider_ID)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print("Created ride table")
    #DONE- WORKS 
    def create_user_account(self, user_type, username, password, name):
        #generate random id
        id = uuid.uuid4().int & (1 << 16) - 1
        print(user_type)
        #create driver account
        if user_type == "D":
            query = '''
            INSERT INTO driver
            VALUES (%s, %s, %s, 0, False, %s)
            '''
            params = (id, username, password, name)
        #create rider account
        else:
            query = '''
            INSERT INTO rider
            VALUES (%s, %s, %s, %s)
             '''
            params = (id, username, password, name)
        self.cursor.execute(query, params)
        self.connection.commit()
        print("Created account")

    #DONE- WORKS 
    def check_user_account(self, user_type, username, password):
        # Choose the appropriate table based on user_type
        if user_type == "D":
            query = '''
            SELECT EXISTS (SELECT 1 FROM DRIVER WHERE username = %s AND password = %s);
            '''
            print("made it past query")
            # Execute the query with parameters to check if the user exists
            self.cursor.execute(query, (username, password))
            
            # Fetch the result
            result = self.cursor.fetchone()

            # Return True if user exists (1) or False if not (0)
            print(result[0])
            self.connection.commit()
            return result[0] == 1
        else:
            query = '''
            SELECT EXISTS (SELECT 1 FROM RIDER WHERE username = %s AND password = %s);
            '''
            # Execute the query with parameters to check if the user exists
            self.cursor.execute(query, (username, password))
            
            # Fetch the result
            result = self.cursor.fetchone()
            self.connection.commit()

            # Return True if user exists (1) or False if not (0)
            return result[0] == 1

    #DONE - WORKS
    # Function to get the driver's average rating
    def get_rating(self, username, password):
        query = '''
        SELECT average_rating FROM DRIVER
        WHERE username = %s AND password = %s;
        '''
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            print(f"Current rating is {result[0]}")
        else:
            print("No rating found for this driver. Please check your login credentials.")

    #DONE - WORKS
    # Function to get a list of all rides provided
    def get_rides(self, user_status, username, password):
    # Get rider or driver ID based on user status
        if user_status == "D":
            query = '''
            SELECT driver_ID
            FROM DRIVER
            WHERE username = %s AND password = %s
            '''
        else:
            query = '''
            SELECT rider_ID
            FROM RIDER
            WHERE username = %s AND password = %s
            '''

        self.cursor.execute(query, (username, password))
        ID = self.cursor.fetchone()

        if not ID:
            print("Account not found or invalid credentials.")
            return

        if user_status == "D":
            driverID = ID[0]  # Get driverID
            query = '''
            SELECT * FROM RIDE
            WHERE driver_ID = %s
            '''
            self.cursor.execute(query, (driverID,))
        else:
            riderID = ID[0]  # Get riderID
            query = '''
            SELECT * FROM RIDE
            WHERE rider_ID = %s
            '''
            self.cursor.execute(query, (riderID,))

        # Fetch the rides
        rides = self.cursor.fetchall()

        if not rides:
            print(f"No rides found for Driver with username {username}.")
            return

            # Print the rides details (this can be customized as needed)
        for ride in rides:
            print(ride)

    #DONE- WORKS
    # Function to update drivers mode from active/inactive
    def change_driver_mode(self, username, password, mode):
        if mode == "A":
            print("TRUE")
            my_bool = True
        else:
            print("FALSE")
            my_bool = False
        update_query = f'''UPDATE DRIVER SET driving_status = %s WHERE username = %s AND password = %s;'''
        self.cursor.execute(update_query, (my_bool, username, password))
        self.connection.commit()
    
    #DONE - WORKS
    def update_driver_rating(self, rating, ride_ID):
        # Update the ride with the current rating
        update_ride_query = '''UPDATE RIDE SET rating = %s WHERE ride_ID = %s;'''
        self.cursor.execute(update_ride_query, (rating, ride_ID))
        self.connection.commit()
        
        # Find the driver associated with the ride
        driver_query = '''
        SELECT driver_ID
        FROM RIDE
        WHERE ride_ID = %s
        '''
        self.cursor.execute(driver_query, (ride_ID,))
        driver_result = self.cursor.fetchone()
        if driver_result is None:
            print("Driver not found for this ride.")
            return
        driver_id = driver_result[0]

        # Calculate the new average rating for the driver
        avg_rating_query = '''
        SELECT AVG(rating)
        FROM RIDE
        WHERE driver_ID = %s
        '''
        self.cursor.execute(avg_rating_query, (driver_id,))
        new_average_rating = self.cursor.fetchone()[0]

        # Update the driver's average rating
        update_driver_query = '''
        UPDATE DRIVER
        SET average_rating = %s
        WHERE driver_ID = %s
        '''
        self.cursor.execute(update_driver_query, (new_average_rating, driver_id))
        self.connection.commit()
        print(f"Driver's average rating updated to {new_average_rating}.")

    #DONE- WORKS
    # Function to match a driver with a rider
    def book_rides(self, username, password):
        # Generate rideID
        ride_id = uuid.uuid4().int & (1 << 16) - 1

        # Find an active driver
        query = '''
        SELECT driver_ID, name
        FROM DRIVER
        WHERE driving_status IS True
        '''
        self.cursor.execute(query)

        # Fetch driver ID
        result = self.cursor.fetchall()

        # Check if any active drivers were found
        if not result:
            print("Could not find an active driver.")
            return
        
        # Assign an active driver from the first tuple in result
        driverID = result[0][0]  # First tuple, first element (driver_ID)
        driverName = result[0][1]  # First tuple, second element (name)

        # Find rider based on username and password
        rider_query = '''
        SELECT rider_ID, name
        FROM RIDER
        WHERE username = %s AND password = %s;
        '''
        self.cursor.execute(rider_query, (username, password))
        rider_result = self.cursor.fetchall()

        # Check if rider account was found
        if not rider_result:
            print("Rider account not found.")
            return
        
        riderID = rider_result[0][0]
        riderName = rider_result[0][1]

        # Prompt for additional ride details
        timestamp = datetime.now()
        pick_up_location = input("Please enter the pickup location: ")
        drop_off_location = input("Please enter drop-off location: ")
        print(f"Ride successfully created with Driver: {driverName} and Rider: {riderName}. "
            f"You traveled from: {pick_up_location} to {drop_off_location} on {timestamp}")
        
        # Rating input
        rating = input("Please rate the ride: ")

        # Insert ride into RIDE table
        insert_query = '''
        INSERT INTO RIDE (ride_id, rating, pickup_location, drop_off_location, time_stamp, driver_id, rider_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (ride_id, rating, pick_up_location, drop_off_location, timestamp, driverID, riderID))
        self.connection.commit()

    #DONE- WORKS
    # Function to find the most recent ride taken
    def find_recent_ride(self, username, password):
        query = '''
        SELECT rider_ID, name
        FROM rider
        WHERE username = %s AND password = %s;'''
        self.cursor.execute(query, (username, password))
        rider_result = self.cursor.fetchall()
        riderID = rider_result[0][0]
        riderName = rider_result[0][1]

        # Ensure 'timestamp' is the correct column name in your schema
        query = '''
        SELECT * 
        FROM RIDE
        WHERE rider_ID = %s
        ORDER BY time_stamp DESC
        LIMIT 1;'''

        self.cursor.execute(query, (riderID,))
        result = self.cursor.fetchall()
        ride_ID = result[0][0]
        rating = result[0][1]
        pickup_location = result[0][2]
        drop_off_location = result[0][3]
        time_stamp = result[0][4]
        driver_id = result[0][5]

        query = '''
        SELECT name
        FROM DRIVER
        WHERE driver_id = %s'''
        self.cursor.execute(query, (driver_id,))
        driver_info = self.cursor.fetchall()
        driver_name = driver_info[0][0]  # Adjust the index based on the schema

        print(f"Ride with Driver: {driver_name} and Rider: {riderName}. You traveled from: {pickup_location} to {drop_off_location} on {time_stamp}. The ride was rated a {rating} out of 10.")
        self.connection.commit()
        return ride_ID



    def show(self):
        query = '''SHOW TABLES;'''
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        else:
            print("No tables found in the database.")

    def delete_everything(self):
        query = '''DROP DATABASE RIDESHARE;'''
        self.cursor.execute(query)


    def close_connection(self):
            self.connection.close()
