from datetime import datetime
import uuid
import mysql.connector

class rideshare_ops():

    def __init__(self):
        self.connection = mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'CPSC408!',
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
        driving_status BOOL DEFAULT False 
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

    def create_user_account(self, user_type, username, password, name):
        #generate random id
        id = uuid.uuid4().int & (1 << 16) - 1
        print(user_type)
        #create driver account
        if user_type == "D":
            query = '''
            INSERT INTO driver
            VALUES (%s, %s, %s, 5, False)
            '''
            params = (id, username, password)
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
            return result[0] == 1
        else:
            query = '''
            SELECT EXISTS (SELECT 1 FROM RIDER WHERE username = %s AND password = %s);
            '''
            # Execute the query with parameters to check if the user exists
            self.cursor.execute(query, (username, password))
            
            # Fetch the result
            result = self.cursor.fetchone()

            # Return True if user exists (1) or False if not (0)
            return result[0] == 1
        
    def get_rating(self, user_type, username, password):
        query = '''
        SELECT average_rating FROM DRIVER
        WHERE username = %s AND password = %s;
        '''
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        print(result)

    def get_rides(self, user_status, username, password):
        #get rider id
        if user_status == "D":
            query = '''
            SELECT driver_ID
            FROM DRIVER
            WHERE %s = username AND password = %s
            '''
        else:
            query = '''
            SELECT rider_ID
            FROM RIDER
            WHERE %s = username AND password = %s
            '''

        self.cursor.execute(query, (username, password))
        if user_status == "D":
            driverID = self.cursor.fetchone()
            query = '''
            SELECT *
            FROM RIDES
            WHERE driver_ID = %s
            '''
            self.cursor.execute(query, driverID)
        else:
            riderID = self.cursor.fetchone()
            query = '''
            SELECT *
            FROM RIDES
            WHERE rider_ID = %s
            '''
            self.cursor.execute(query, riderID)

    def change_driver_mode(self,username, password, mode):
        if mode == "A":
            my_bool = True
        else:
            my_bool = False
        update_query = f'''UPDATE DRIVER SET driving_status = %s WHERE username = %s AND password = %s;'''
        self.cursor.execute(update_query, (my_bool, username, password))
        self.connection.commit()

#function to match a driver with a rider
    def find_rides(self, username, password, pick_up_location, drop_off_location, rating):
        #generate rideID
        ride_id = uuid.uuid4().int & (1 << 16) - 1
        #find active driver
        query = '''
        SELECT driver_ID
        FROM DRIVER
        WHERE driving_status = True
        '''
        #execute query
        self.cursor.execute(query)

        #fetch driver ID
        result = self.cursor.fetchone()

        #check if any active drivers were found
        if result == None:
            print("Could not find an active driver")
            return
        
        #assign an active driver from tuple
        driverID = result[0]
        rider_query = '''
        SELECT rider_ID
        FROM RIDER
        WHERE username = %s AND password = %s;'''
        self.cursor.execute(rider_query, (username, password))
        rider_result = self.cursor.fetchone()

        if rider_result is None:
            print("Rider account not found.")
            return
        riderID = rider_result[0]
        timestamp = datetime.now()
        #
        # CREATE TABLE RIDE(
        # ride_ID INT PRIMARY KEY NOT NULL,
        # rating INT,
        # pickup_location VARCHAR(60),
        # drop_off_location VARCHAR(60),
        # time_stamp TIMESTAMP,
        # driver_id INT,
        # rider_id INT,
        # FOREIGN KEY (driver_ID) REFERENCES DRIVER(driver_ID),
        # FOREIGN KEY (rider_ID) REFERENCES RIDER(rider_ID)
        insert_query = '''
        INSERT INTO RIDE (ride_id, rating, pickup_location, drop_off_location, time_stamp, driver_id, rider_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query,(ride_id, rating, pick_up_location, drop_off_location, timestamp, driverID, riderID))
        self.connection.commit()
        print(f"Ride successfully created with Driver ID {driverID} and Rider ID {riderID}.")

    
    def find_recent_ride(self,user_status, username, password):
        query = '''
        SELECT riderID
        FROM rider
        WHERE username = %s AND password = %s;'''
        self.cursor.execute(query, (username, password))
        riderID = self.cursor.fetchone()

        query = '''
        SELECT * 
        FROM RIDE
        WHERE riderID = %s
        ORDER BY timestamp DESC
        LIMIT 1;'''

        self.cursor.execute(query, riderID)
        result = self.cursor.fetchone()
        print(result)

    def delete_everything(self):
        query = '''DROP DATABASE RIDESHARE;'''
        self.cursor.execute(query)


    def close_connection(self):
            self.connection.close()
