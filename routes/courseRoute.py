from flask import request,Blueprint,jsonify
from models.coursemodel import Course
from middlewares.auth_middleware import auth_middleware
from middlewares.auth_admin_student_middleware import auth_admin_student_middleware
course_bp=Blueprint('Course',__name__)
@course_bp.route("/create-course",methods=["POST"])
@auth_middleware
def create_course():
    try:
        data=request.get_json()
        if data:
            course=Course(
                course_name=data["course_name"],
                img=data["img"],
                duration=data["duration"],
                price=data["price"],
                mode=data["mode"],
                road_map_id=data["road_map_id"]
            )
            result=course.save()
            if result:
                return jsonify({"message":"course created successfully"}),200
            else:
                return jsonify({"message":"error while creating course"}),204
    except:
        return jsonify({"message":"internal server error"}),500

@course_bp.route("/get-all-courses",methods=["GET"])
# @auth_admin_student_middleware
def get_all_courses():
    try:
        data=Course.objects().only("course_name","img","duration","price","mode","road_map_id")
        if data:
            coursedata=[]
            for course in data:
                coursedata.append({
                    "id":str(course.id),
                    "course_name":course.course_name,
                    "img":course.img,
                    "duration":course.duration,
                    "price":course.price,
                    "mode":course.mode,
                    "road_map_id":course.road_map_id

                })
            return jsonify({"data":coursedata,"message":"courses fetched successfully"})
    except:
        return jsonify({"message":"internal server error"}),500

@course_bp.route("/get-course/<id>",methods=["GET"])
@auth_admin_student_middleware
def get_courses(id):
    try:
        course=Course.objects(id=id).first()
        if course:
            course_data={
                "course_name":course.course_name,
                "img":course.img,
                "duration":course.duration,
                "price":course.price,
                "mode":course.mode,
                "road_map_id":course.road_map_id
            }
            return jsonify({"message":"course fetched successfully","data":course_data})
        else:
            return jsonify({"message":"error while fetchin get course api"})    
    except:
        return jsonify({"message":"internal server error"}),500

@course_bp.route("/update-course/<id>",methods=["PUT"])
# @auth_middleware
def update_courses(id):
    try:
        data=request.get_json()
        if data:
            course=Course.objects(id=id)
            if course:
                result=course.update(**data)
                if result:
                    return jsonify({"message":"course updated successfully!"}),200
                else:
                    return jsonify({"message":"error while updating course!"}),204
            else:
                return jsonify({"message":"course not found!"}),204
        else:
            return jsonify({"message":"eoor while updating data!"}),204
    except:
        return jsonify({"message":"internal server error"}),500
    
@course_bp.route("/delete-course/<id>",methods=["DELETE"])
@auth_middleware
def delete_courses(id):
    try:
        data=Course.objects(id=id).first()
        if data:
            result=data.delete()
            if result==None:
                return jsonify({"message":"course deleted successfully"}),200
            else:
                return jsonify({"message":"error while deleting the data"}),204
        else:
            return jsonify({"message":"course not found"}),204
    except:
        return jsonify({"message":"internal server error"}),500



   
