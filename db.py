mport uuid
import mysql.connector
conn = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = 'HenryCPSC408',
                               auth_plugin = 'mysql_native_password',
                               database = 'RideShare')
#Cursor object to interact with database
cur_obj = conn.cursor()


class rideshare_ops():

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

        #create ride table
        query = '''
        CREATE TABLE RIDE(
        ride_ID INT PRIMARY KEY NOT NULL,
        rating INT,
        pickup_location VARCHAR(60),
        drop_off_location VARCHAR(60),
        time_stamp TIMESTAMP,
        FOREIGN KEY (driver_ID) REFERENCES driver(driver_ID),
        FOREIGN KEY (rider_ID) REFERENCES rider(rider_ID)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print("Created ride table")

        #create rider table
        query = '''
        CREATE TABLE RIDER(
        rider_ID INT PRIMARY KEY NOT NULL,
        username VARCHAR(30) UNIQUE NOT NULL,
        password VARCHAR(30) NOT NULL,
        name VARCHAR(30) NOT NULL,
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print("Created rider table")

    def create_account(self, user_type, username, password):
        #generate random id
        id = uuid.uuid1()
        if user
        #create rider account
        elif user_type == "R":
            query = '''
            INSERT INTO rider
            VALUES ({id.int}, {username}, {password}, {name})

        '''
conn.close()
