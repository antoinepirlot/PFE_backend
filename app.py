from services.CoursesService import CoursesService
from services.UsersService import UsersService
from models.Course import Course

from flask import Flask, jsonify, request

from flask_cors import CORS

from routes import test, user

app = Flask(__name__)
cors = CORS(app)
courses_service = CoursesService()
users_service = UsersService()


#Routes
app.register_blueprint(test.route, url_prefix="/")
app.register_blueprint(user.route, url_prefix="/")

@app.route("/createCourse", methods=["POST"])
def create_course():
    # check body is not empty
    if request.json['id_category'] is None or request.json['id_category'] < 1 or \
            request.json['id_teacher'] is None or request.json['id_teacher'] < 1 or \
            request.json['course_description'] is None or len(str(request.json['course_description']).strip()) == 0 or \
            request.json['price_per_hour'] is None or request.json['price_per_hour'] <= 0 or \
            request.json['city'] is None or len(str(request.json['city']).strip()) == 0 or \
            request.json['country'] is None or len(str(request.json['country']).strip()) == 0 or \
            request.json['id_level'] is None or request.json['id_level'] < 1:
        return "Course is not in the good format", 400

    new_course = Course(request.json['id_category'], request.json['id_teacher'], request.json['course_description'],
                        request.json['price_per_hour'], request.json['city'], request.json['country'],
                        request.json['id_level'])
    return courses_service.create_one_course(new_course)





if __name__ == '__main__':
    app.run()
