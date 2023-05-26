from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    return "WELCOME TO FLASK"


@app.route('/spam')
def check_spam():
    args = request.args
    print(args.get('comment'))
    return "CHECKING SPAM"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
