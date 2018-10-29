import os
import time
from flask import Flask, render_template, make_response, send_from_directory
from werkzeug.wrappers import AuthorizationMixin
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from config import SENTRY_SDK_KEY

sentry_sdk.init(
    dsn=SENTRY_SDK_KEY,
    integrations=[FlaskIntegration()]
)

# creates a Flask application, named app
app = Flask(__name__)

# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    timestamp = int(time.time() * 1000)
    resp = make_response(render_template('index.html', timestamp=timestamp))
    return resp

# run the application
if __name__ == "__main__":  
    # app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')
    app.run(host='localhost', debug=True)
