import simple_websocket
from flask_cors import CORS
from flask import Flask, request, jsonify
from scan_delete_insta_spam import SpamBot
from flask_sock import Sock
import time
import json

app = Flask(__name__)
CORS(app)
bot = SpamBot(insta_scanner=True)
sock = Sock(app)


@sock.route('/sub')
def test_sub(ws):
    alive = True
    try:
        while alive:
            time.sleep(30)
            result = bot.scan_insta()
            json_res = json.dumps(result, indent=4)
            print(json_res)
            ws.send(json_res)
            # ws.send('{"msg": "Hello World from the websocket!"}')
    except simple_websocket.ConnectionClosed:
        print('Socket Closed....')
        alive = False


@app.route('/')
def home():
    return "WELCOME TO FLASK"


@app.route('/update')
def update_insta():
    result = bot.scan_insta()
    print(result)
    return jsonify(result)


@app.route('/spam')
def check_spam():
    args = request.args
    comment = args.get('comment')
    is_spam = bot.is_spam(comment)
    reply = {"msg": comment, "isSpam": is_spam}
    return jsonify(reply)


if __name__ == "__main__":
    app.run(port=5000)
