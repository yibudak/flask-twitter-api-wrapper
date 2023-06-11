from flask import Flask, jsonify, request
from config import Config
from wrapper import TwitterWrapper

conf = Config("/etc/twitter-api.conf")
app = Flask(__name__)
API = TwitterWrapper(conf)

# ENDPOINTS


@app.route("/getTweetById", methods=["GET"])
def get_tweet_by_id() -> dict:
    response = {"status": "error"}  # default response

    if request.args.get("apiKey") == conf.app.API_KEY:
        tweet_id = request.args.get("tweetId")
        if tweet_id:
            try:
                data = API.get_tweet(tweet_id)
                response["status"] = "success"
                response["data"] = data
            except Exception as e:
                response["error"] = str(e)

    return jsonify(response)
