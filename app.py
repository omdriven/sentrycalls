import os
import time
from pprint import pprint
import json
import requests
from flask import Flask, render_template, make_response, send_from_directory
from werkzeug.wrappers import AuthorizationMixin
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from config import APP_HOST, SENTRY_SDK_KEY, SENTRY_AUTH_TOKEN, ORG_SLUG, PROJECT_SLUG, TEST_EVENT_CODE

sentry_sdk.init(
    dsn=SENTRY_SDK_KEY,
    integrations=[FlaskIntegration()]
)

# creates a Flask application
app = Flask(__name__)

# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    timestamp = int(time.time() * 1000)
    resp = make_response(render_template('index.html', timestamp=timestamp, data="Index route"))
    return resp

@app.route("/projects")
def projects():
    url = 'https://sentry.io/api/0/projects/'
    headers = {'Authorization': 'Bearer {auth_token}'.format(auth_token=SENTRY_AUTH_TOKEN)}

    pprint(headers)

    # call sentry
    r = requests.get(url, headers=headers)

    timestamp = int(time.time() * 1000)

    # prepare data from sentry to render on page
    data = json.loads(r.content)
    pprint(data)
    resp = make_response(render_template('index.html', timestamp=timestamp, data=data))
    return resp

@app.route("/custom_event")
def custom_event():
    url = 'https://sentry.io/api/0/projects/{org_slug}/{project_slug}/events/{event_code}/'.format(
        org_slug=ORG_SLUG, project_slug=PROJECT_SLUG, event_code=TEST_EVENT_CODE)

    headers = {'Authorization': 'Bearer {auth_token}'.format(auth_token=SENTRY_AUTH_TOKEN)}

    pprint(headers)

    r = requests.get(url, headers=headers)

    timestamp = int(time.time() * 1000)
    data = json.loads(r.content)
    pprint(data)
    resp = make_response(render_template('index.html', timestamp=timestamp, data=data))
    return resp

# run the application
if __name__ == "__main__":  
    # app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')
    app.run(host=APP_HOST, debug=True)
