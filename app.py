from flask import Flask
import services.CoursesService as CoursesService

app = Flask(__name__)
courses_service = CoursesService.CoursesService()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/createCourse", methods=["POST"])
def create_course():
    return courses_service.create_one_course(None)


if __name__ == '__main__':
    app.run()
