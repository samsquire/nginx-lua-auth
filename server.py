import os
import re
import redis
import uuid
import json
from argparse import ArgumentParser

from flask import Flask, request, make_response, redirect

app = Flask(__name__)

parser = ArgumentParser()
parser.add_argument("--nothing")
args = parser.parse_args(os.environ["SERVER_ARGS"].split(" "))

r = redis.Redis()

@app.route("/")
def shard(userid=""):
    session_cookie = request.cookies.get('session')
    if session_cookie and r.hget(session_cookie, "logged_in"):
        return redirect("/")
    return """
    <form method="POST" action="/auth/login">
    <input name="username" type="text" placeholder="username"/>
    <input name="password" type="password" placeholder="username"/>
    <button type="submit">Login</button>
    </form>
    """

@app.route("/main")
def main():
    session_id = request.cookies.get('session')
    if session_id and r.hget(session_id, "logged_in"):
        # logged in
        username = r.hget(session_id, "username")
        r.expire(session_id, time="60")
        return """
        Logged in as {}
        """.format(username)
    else:
        print("Could not login")	
        return "not logged in"    


def sanitize(unsafe):
    safe = re.sub('[^0-9a-zA-Z]+', '', unsafe)
    return safe

@app.route("/login", methods=["POST"])
def login():
    users = json.loads(open("users.json").read())
    unsafe_username = request.form["username"]
    unsafe_password = request.form["password"]

    safe_username = sanitize(unsafe_username)
    safe_password = sanitize(unsafe_password)
    if users.get(safe_username) != None and safe_password == "sam": 
        session_id = uuid.uuid4().hex
        r.hset(session_id, "logged_in", "1") 
        r.hset(session_id, "username", safe_username) 
        resp = make_response(redirect("/"))
        r.expire(session_id, time="60")
        resp.set_cookie('session', session_id)
        f = open("/etc/nginx/sessions/{}".format(session_id), "w")
        f.write(request.headers.getlist("X-Forwarded-For")[0])
        f.close()
        return resp 
    else:
        return "bad login"
