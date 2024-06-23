import pymongo 
import os
from dotenv import load_dotenv

load_dotenv()

uri=os.getenv('MONGO_URI')

client = pymongo.MongoClient(uri)



def close_connection():
    client.close()
    print("Connection with DB closed")

