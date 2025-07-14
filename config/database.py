# from pymongo import MongoClient
# try:
#     client=MongoClient("mongodb://localhost:27017")
#     database=client["lms"]
#     users=database["users"]
#     print("db connected")
# except:
#     print("db not connected")
import os
from mongoengine import connect

def connect_db():
    connect(
        host=os.getenv("MONGO_DB"),
        alias="default"
    )
    print("connected✅")
    
