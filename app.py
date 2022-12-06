import database
import users.dao

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

database.initialiseConnection()
@app.route('/')
def hello_world():  # put application's code here
  return 'Hello World!'

@app.route('/util', methods=['GET'])
def get_users():
    try:

        result = users.dao.getUsers()
        return jsonify({'users': result}), 200
    except (Exception) as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


if __name__ == '__main__':
  app.run()
