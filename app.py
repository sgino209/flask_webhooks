#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Danit Gino, October-2021, danitgino@yahoo.com

# Run server:
# % python app.py

# Test (from another terminal):
# % curl -X POST http://127.0.0.1:5000/api/print?p=singleString
# % curl -X POST http://127.0.0.1:5000/api/sum?"a=1&b=2"

from flask import Flask, request
import json
import re


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 to see a message
    """
    return ('This is a website.', 200, None)


@app.route('/api/print', methods=['GET', 'POST'])
def print_test():
    """
    Send a POST request to localhost:5000/api/print with a JSON body with a "p" key
    to print that message in the server console.
    """
    payload = request.args.get('p')
    resp = json.dumps({'res': payload})
    print('Got:', payload)
    print('Rsp:', resp)
    return (resp, 200, None)


@app.route('/api/sum', methods=['GET', 'POST'])
def sum():
    """
    Send a POST request to localhost:5000/api/sum with a JSON body with an "a" and "b" key
    to have the app add those numbers together and return a response string with their sum.
    """
    payload = request.args
    a = int(payload.get('a'))
    b = int(payload.get('b'))
    res = a + b
    resp = json.dumps({'a': a, 'b': b, 'res': res})
    print('Got:', a, b)
    print('Rsp:', resp)
    return (resp, 200, None)


if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)
