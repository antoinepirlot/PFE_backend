import donnees.UserDao as UserDao
import services.CoursesService as CoursesService

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
courses_service = CoursesService.CoursesService()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/createCourse", methods=["POST"])
def create_course():
    return courses_service.create_one_course(None)


@app.route('/users', methods=['GET'])
def get_users():
    try:
        result = UserDao.getUsers()
        return jsonify({'users': result}), 200
    except (Exception) as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500

@app.route('/users/<int:id_user>', methods=['GET'])
def get_user_by_id(id_user):
    try:
        result = UserDao.getUserById(id_user)
        return jsonify({'users': result}), 200
    except (Exception) as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500

@app.route('/users', methods=['POST'])
def add_user():
    try:
        UserDao.singInUser(request.json)
        return jsonify({'user': 'user created'}), 201
    except (Exception) as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


if __name__ == '__main__':
    app.run()
