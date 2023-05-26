from flask import Flask, request, jsonify
from scan_delete_insta_spam import SpamBot


app = Flask(__name__)
bot = SpamBot()


@app.route('/')
def home():
    return "WELCOME TO FLASK"


@app.route('/spam')
def check_spam():
    args = request.args
    comment = args.get('comment')
    is_spam = bot.is_spam(comment)
    reply = {"msg": comment, "isSpam": is_spam}
    return jsonify(reply)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
