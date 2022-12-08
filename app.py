from flask import Flask

from routes import test

app = Flask(__name__)


#Routes
app.register_blueprint(test.route, url_prefix="/")

if __name__ == '__main__':
  app.run()
