#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Shahar Gino, October-2021, sgino209@gmail.com

# Run server:
# % python app.py

# Test (from another terminal):
# % curl -X POST http://127.0.0.1:5000/api/print?p=singleString
# % curl -X POST http://127.0.0.1:5000/api/sum?"a=1&b=2"
# % curl -X POST http://127.0.0.1:5000/api/print_json -H 'Content-Type: application/json' -d '{"a":"hello", "b":"world", "c":"17"}'

import json
import pandas as pd
from os import environ
from flask import Flask, request


app = Flask(__name__)

app.config['FOO'] = environ.get('FOO')

# -----------------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 to see a message
    """
    return ('This is a website', 200, None)

# -----------------------------------------------------------------------------------

@app.route('/api/print', methods=['POST'])
def print():
    """ Get a parameter and return it as a response """
    payload = request.args.get('p')
    resp = json.dumps({'res': payload})
    print('Got:', payload)
    print('Rsp:', resp)
    print('FOO:', app.config['FOO'])
    return (resp, 200, None)

# -----------------------------------------------------------------------------------

@app.route('/api/print_json', methods=['POST'])
def print_json():
    """ Similar to print function, just with a JSON interface and DataFrame manipulation """
    payload = request.get_json()
    df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
    result = df.to_json(orient="split")
    parsed = json.loads(result)
    resp = json.dumps(parsed)
    print('Got:', payload)
    print('Rsp:', resp)
    return (resp, 200, None)

# -----------------------------------------------------------------------------------

@app.route('/api/sum', methods=['POST'])
def sum():
    """ Get 2 numbers and return their summation """
    payload = request.args
    a = int(payload.get('a'))
    b = int(payload.get('b'))
    res = a + b
    resp = json.dumps({'a': a, 'b': b, 'res': res})
    print('Got:', a, b)
    print('Rsp:', resp)
    return (resp, 200, None)

# -----------------------------------------------------------------------------------

if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)

