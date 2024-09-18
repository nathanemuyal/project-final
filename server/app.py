import base64
from flask import Flask, request, redirect, jsonify
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()


from firebase import user_login

app = Flask(__name__)
CORS(app)

# Your Google credentials
CLIENT_ID = os.getenv('REACT_APP_CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/auth/callback'  # Redirect URI in Google Cloud settings
TOKEN_URL = 'https://oauth2.googleapis.com/token'

@app.route('/auth/callback')
def oauth2callback():
    # Get the authorization code from the request
    code = request.args.get('code')
    if not code:
        return 'Authorization code not found', 400

    # Exchange the authorization code for access and refresh tokens
    token_data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    # Exchange the code for tokens
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()

    if 'access_token' not in token_json:
        return jsonify({'error': 'Failed to obtain access token'}), 400

    access_token = token_json['access_token']


    # Step 2: Retrieve user email using the access token
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    userinfo_response = requests.get(userinfo_url, headers=headers)
    user_info = userinfo_response.json()

    # Get the user's email and display name from the response
    user_email = user_info.get('email')
    display_name = user_info.get('name')  # This retrieves the display name

    if not user_email or not display_name:
        return jsonify({'error': 'Failed to obtain user email and display name'}), 400

    handle_user(access_token, user_email, display_name)
    return redirect(f'http://localhost:3000/?token={access_token}')


def handle_user(access_token, user_email, display_name):
    user_login(user_email, display_name)


if __name__ == '__main__':
    app.run(debug=True)