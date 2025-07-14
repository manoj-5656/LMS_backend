from functools import wraps
import jwt
import os
from models.usermodel import user
from flask import jsonify,request
def auth_admin_student_middleware(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        token=request.cookies.get('token')
        if token:
            validate=jwt.decode(token,os.getenv("jwt_key"),algorithms="HS256")
            
            if validate:
                User=user.objects(id=validate["id"])
                if User[0]["role"]==1 or User[0]["role"]==0 :
                    return func(*args,**kwargs)
                else:
                    return jsonify({"message":"access denied"}),401
            else:
                return jsonify({"message":"token not found"})
        else:
            return jsonify({"message":"access denied"}),401
    return wrapper