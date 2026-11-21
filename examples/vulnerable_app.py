"""
INTENTIONALLY VULNERABLE - FOR DEMONSTRATION ONLY. DO NOT USE.

A small fake web app with security mistakes planted on purpose,
so the security agent (and Bandit) have something to find.
All secrets here are fake placeholders.
"""

import hashlib
import pickle
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, request

app = Flask(__name__)

# Mistake 1: secret written in the code (fake value)
API_KEY = "sk-FAKE-1234567890-NOT-A-REAL-KEY"
ADMIN_PASSWORD = "admin123"


@app.route("/user")
def get_user():
    # Mistake 2: SQL built by joining text (SQL injection)
    name = request.args.get("name", "")
    conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    return str(conn.execute(query).fetchall())


@app.route("/ping")
def ping():
    # Mistake 3: shell command built from user input (command injection)
    host = request.args.get("host", "localhost")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/calc")
def calc():
    # Mistake 4: eval on user input (code injection)
    return str(eval(request.args.get("expr", "1+1")))


def hash_password(password):
    # Mistake 5: weak hash for passwords
    return hashlib.md5(password.encode()).hexdigest()


@app.route("/load", methods=["POST"])
def load():
    # Mistake 6: unsafe deserialization of user data
    return str(pickle.loads(request.data))


def read_config(path):
    # Mistake 7: unsafe YAML loading
    with open(path) as f:
        return yaml.load(f, Loader=yaml.Loader)


def fetch_report(url):
    # Mistake 8: HTTPS certificate check turned off
    return requests.get(url, verify=False, timeout=10).text


if __name__ == "__main__":
    # Mistake 9: debug mode on, listening on all addresses
    app.run(host="0.0.0.0", debug=True)
