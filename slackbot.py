import flask
from urllib.parse import urlencode
import requests

with open('client_id') as client_id_file:
    client_id = client_id_file.read().strip()

with open('client_secret') as client_secret_file:
    client_secret = client_secret_file.read().strip()

local_host = 'localhost'
local_port = 5050

redirect_uri = 'http://{}:{}/authentication'.format(local_host, local_port)

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    query = urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
    })
    return flask.redirect('https://slack.com/oauth/authorize?' + query)

@app.route('/authentication', methods=['GET'])
def authentication():
    args = flask.request.args
    if 'error' in args:
        error = args['error']
        return 'Error: {}'.format(error)

    if 'code' in args:
        code = args['code']
        data = requests.get('https://slack.com/api/oauth.access', params={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
        }).json()
        access_token = data['access_token']
        return 'Access token: {}'.format(access_token)

app.run(port=local_port, debug=True)

