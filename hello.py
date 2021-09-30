from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return r"<a href='api/v1/hello-world-29'><h1>api/v1/hello-world-29</h1></a>"


@app.route("/api/v1/hello-world-29")
def hello_world():
    return r"<h1>Hello World 29!</h1>"


if __name__ == '__main__':
    app.run()