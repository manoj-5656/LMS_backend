from flask import Flask,request,jsonify,render_template
from flask_cors import CORS
from config.database import connect_db
from routes.authRoutes import auth_bp
from routes.courseRoute import course_bp

app=Flask(__name__)
CORS(app,supports_credentials=True,origins="http://localhost:5173")
connect_db()

@app.route('/',methods=['GET'])
def home():
    return "this is from local host 4000"

app.register_blueprint(auth_bp,url_prefix='/api/auth')
app.register_blueprint(course_bp,url_prefix='/api/course')





    
   


if __name__=="__main__":
    app.run(host="localhost",port=4000,debug=True)
