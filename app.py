from flask import Flask, jsonify, request

from flask_cors import CORS

from routes import courses, users

app = Flask(__name__)
cors = CORS(app)

# Routes
app.register_blueprint(courses.route, url_prefix="/courses")
app.register_blueprint(users.route, url_prefix="/users")

if __name__ == '__main__':
    app.run()
