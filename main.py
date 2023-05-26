from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "WELCOME TO FLASK"


@app.route('/spam')
def check_spam():
    return "CHECKING SPAM"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
