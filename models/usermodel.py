from mongoengine import Document,StringField,EmailField,IntField,ListField
import datetime

class user(Document):
    name=StringField(required=True,max_length=20)
    email=EmailField(required=True,unique=True)
    ph_no=StringField(required=True,max_length=10)
    password=StringField(required=True)
    role=IntField(default=0)
    purchased_courses=ListField()
    created_at=StringField(default=str(datetime.datetime.now()))
    university_name=StringField(default="lms")
    meta={
        "collection":"user",
        "db_alias":"default"
    }