from flask import Blueprint,request,jsonify,make_response
from models.usermodel import user
from middlewares.auth_student_middleware import auth_student_middleware
from middlewares.auth_middleware import auth_middleware
import os
from middlewares.auth_admin_student_middleware import auth_admin_student_middleware
import bcrypt
import jwt
import datetime

auth_bp=Blueprint('auth',__name__)

@auth_bp.route("/signup",methods=["POST"])
def signup():
    data=request.get_json()
    
    hash_password=bcrypt.hashpw(data["pwd"].encode(),bcrypt.gensalt()).decode()
    if data:
       try:
           users=user(
               name=data['name'],
               email=data['email'],
               ph_no=data['ph_no'],
               password=hash_password 
           ) 
           users.save()
           return jsonify({"message":"Signup Successfull"})
       except:
           return jsonify({"message":"database error!"})
    else:
        return "data not received"
    
    
@auth_bp.route("/signin",methods=["POST"])
def signin():
    data=request.get_json()
    try:
        email_check=user.objects(email=data["email"]).first()
        if email_check:
            password_valid=bcrypt.checkpw(data["password"].encode(),email_check.password.encode())
            if password_valid:
                 token=jwt.encode({"id":str(email_check.id),"exp":datetime.datetime.utcnow()+datetime.timedelta(1)},os.getenv("jwt_key"),algorithm="HS256")
                 response=make_response(jsonify({"message":"Signin Successfull"}),200)
                 response.set_cookie( "token",token,httponly=False,secure=False,samesite="LAX")
                 response.set_cookie( "id",str(email_check.id),httponly=False,secure=False,samesite="LAX")
                 return response
            else:
                response=make_response(jsonify({"message":"invaild password"}))
                return response
        else:
            response=make_response(jsonify({"message":"invalid email"}))
            return response
    except:
        response=make_response(jsonify({"message":"database error from signin"}))
        return response
    
@auth_bp.route("/getusers",methods=["GET"])
@auth_middleware
def get_users():
    try:
        data=user.objects().only("name","id","email","ph_no","role","created_at","university_name")
        if data:
        # print(data)
            users=[]
            for i in data:
                users.append({
                    "id":str(i.id),
                    "name":i.name,
                    "email":i.email,
                    "ph_no":i.ph_no,
                    "role":i.role,
                    "created_at":i.created_at,
                    "university_name":i.university_name
                })
            return jsonify({"data":users}),200
        else:
            return jsonify({"data not found"}),401
    except:
        return jsonify({"Internal server error"}),500

@auth_bp.route('/update-users/<id>',methods=["PUT"])
@auth_admin_student_middleware
def update_data(id):
    try:
        update_data=request.get_json()
        if update_data:
            User=user.objects(id=id)
            if User:
                result=User.update(**update_data)
                if result:
                    return jsonify({"message":"update successfull"}),200
                else:
                    return jsonify({"message":"error in updating data"}),204
            else:
                return jsonify({"message":"user not found"}),204
        else:
            return jsonify({"message":"data not found"}),204
    except:
        return jsonify({"message":"Internal server error"}),500
    
@auth_bp.route('/get-user/<id>',methods=["GET"])
@auth_admin_student_middleware
def get_user(id):
    try:
        users=user.objects(id=id).only("name","id","email","ph_no","role","created_at").first()
        if users:
            user_data={
                "role":users.role,
                "name":users.name,
                "email":users.email,
                "ph_no":users.ph_no,
                "created_at":users.created_at,
                "id":str(users.id),
                "university_name":users.university_name
            }
            return jsonify({"message":"user fetched successfully","data":user_data}),200
        else:
            return jsonify({"message":"user not found"}),204
    except:
        return jsonify({"message":"internal server error"}),500
        
@auth_bp.route('/deleteuser/<id>',methods=["DELETE"]) 
@auth_middleware
def delete_user(id):
    try:
        data=user.objects(id=id).first()
        print(data)
        if data:
            result=data.delete()
            
            if result==None:
                return jsonify({"message":"data deleted successfully"})
            else:
                return jsonify({"message":"error in deleting data"})
        else:
            return jsonify({"message":"User not found"})
    except:
        return jsonify({"message":"Internal server error"})

@auth_bp.route("/signout",methods=["POST"])
def sign_out():
    response=make_response("deleted")
    response.delete_cookie("token")
    response.delete_cookie("id")
    return response

@auth_bp.route('/payment/<id>',methods=["PUT"])
@auth_admin_student_middleware
def payment(id):
    data=request.get_json()
    if data:
        users=user.objects(id=id).first()
        if users:
            users.purchased_courses.append(data)
            users.save()
            return jsonify({"message":"payment successfull"})
        else:
            return jsonify({"message":"user not found"})



    