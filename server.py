from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config.database import connect_db
from routes.authRoutes import auth_bp
from routes.courseRoute import course_bp
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, origins="https://lms-jawn.vercel.app")
connect_db()

@app.route('/', methods=['GET'])
def home():
    return "this is from deployed backend"

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(course_bp, url_prefix='/api/course')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use environment PORT or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
