import os
from flask import Flask, redirect, url_for, request, session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up OAuth credentials and scopes
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')  # Can be set from environment variables or directly
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')  # Can be set from environment variables or directly
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Secure Flask secret key from environment

@app.route('/')
def index():
    return 'Welcome to the app!'

@app.route('/login')
def login():
    # Create the OAuth flow object with the client ID and client secret
    flow = InstalledAppFlow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = url_for('callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account'
    )

    # Save the state so we can verify the request later
    session['state'] = state

    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Verify the request state
    if request.args.get('state') != session['state']:
        raise Exception('Invalid state')

    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        state=session['state']
    )
    flow.redirect_uri = url_for('callback', _external=True)

    # Exchange the authorization code for an access token
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials to the session
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Clear the session (logging out the user)
    session.clear()
    return redirect(url_for('index'))

# Utility function to convert credentials to dictionary
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    app.run(debug=True, port=5001)
