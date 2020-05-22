#!/usr/bin/env python3

import flask
import requests

import libyiban
import libyiban_ex

QAPP_ID = 674301
CTFD_BASE = 'http://127.0.0.1:4000'
CTFD_TOKEN = 'EZFOREVER_ABUSES_ZHAMAO_PLUGIN'

with open('demo2_index.htm', 'r') as f:
    INDEX_CONTENT = f.read()

app = flask.Flask(__name__)
account = libyiban.YiBanAccount()
commenter = libyiban_ex.QAppCommenter(account, QAPP_ID)

@app.route('/')
def route_index():
    return flask.render_template_string(INDEX_CONTENT, ctfd_base = CTFD_BASE)

@app.route('/api/scoreboard')
def route_api_scoreboard():
    ''' This route is here solely for working around the CORS policy. '''
    return flask.jsonify(requests.get(CTFD_BASE + '/api/v1/scoreboard/top/10').json())

@app.route('/api/zmpush', methods = ['POST'])
def route_api_zmpush():
    if not flask.request.is_json:
        flask.abort(400)
    req_data = flask.request.json
    if 'token' not in req_data.keys() or 'ctf_message' not in req_data.keys():
        flask.abort(400)
    if req_data['token'] != CTFD_TOKEN:
        flask.abort(403)
    commenter.new_comment(req_data['ctf_message'])
    return {}

def main():
    app.run(debug = True, host = '127.0.0.1', port = 3457)
    return 0

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        exit(130)

