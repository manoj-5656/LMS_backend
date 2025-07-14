from mongoengine import Document,StringField,EmailField

import datetime

class Course(Document):
    course_name=StringField(required=True,max_length=20)
    img=StringField(required=True)
    duration=StringField(required=True,max_length=2)
    price=StringField(required=True)
    mode=StringField(default="onine")
    road_map_id=StringField(default="lms")
    created_at=StringField(default=str(datetime.datetime.now()))
    meta={
        "collection":"course",
        "db_alias":"default"
    }