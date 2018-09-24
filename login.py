import pymongo
import hashlib
import string
import random

class User:
    # Initialize
    def __init__(self):

        try:
            # Make a connection to the Database running on localhost at port 27017
            # Database name skylark
            # Collection name users
            self.connection=pymongo.MongoClient('localhost:27017')
            self.db=self.connection.skylark
            self.users=self.db.users
        except:
            print("Connection failed!")
        
    # Make salt for the password
    def make_salt(self):
        salt=""
        # Create a 6 digit hashcode
        for i in range(6):
            salt+=random.choice(string.ascii_letters)

        return salt

    def create_hashed_password(self,password,salt=None):
        if(salt==None):
            salt=self.make_salt()
        # Encode the object
        temp=(str(password)+salt).encode('UTF-8')
        # SHA_512 Encoded object
        hex_temp=hashlib.sha3_512(temp).hexdigest()
        password_hashed=hex_temp+";"+salt

        return password_hashed

    def find_user(self,email):
        find={"_id":email}
        try:
            profile=self.users.find_one(find)
            self.connection.close()
            return profile
        except Exception as e:
            print(e)
            self.connection.close()
            # No such profile found.
            return 400

    def add_user(self,name,email,password):
        hashed_password=self.create_hashed_password(password)
        profile={"_id":email,'name':name,'password':hashed_password}
        try:
            self.users.insert_one(profile)
            print("New registration")
            self.connection.close()
            return 200
        except Exception as e:
            # Duplicate key Error, There is already a user with the same email id.
            self.connection.close()
            return 300

    def login(self,email,password):

        find={"_id":email}
        profile=self.users.find_one(find)
        # Retrieve the actual password from the profile.
        actual_password=profile['password']

        # Extract the salt on the actual password
        actual_salt=actual_password.split(';')[1]
        entered_password=self.create_hashed_password(password,actual_salt)
        self.connection.close()
        if(entered_password==actual_password):
            # Verified User.
            return 200
        else:
            # Incorrect password.
            return 300


# UNIT TEST CODE
#u=User()
#name='prateek'
#email='prateekbedi96@gmail.com'
#password=1234

#u.add_user(name,email,password)
#print(u.login(email,password))
#print(u.find_user(email))
