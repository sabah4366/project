import requests
from django.conf import settings

def get_token(code):
    token_url = 'https://{settings.AUTH0_DOMAIN}/oauth/token'

    response = requests.post(
        token_url,
        json={
            'grant_type': 'authorization_code',
            'client_id': '{settings.AUTH0_CLIENT_ID}',
            'client_secret': '{settings.AUTH0_CLIENT_SECRET}',
            'code': code,
            'redirect_uri': 'http://localhost:8000/callback/',
        }
    )

    # Check if the request was successfu
    if response.status_code == 200:
        # Extract the token from the response JSON
        token = response.json().get('access_token')
        return token

    # Return None
    return None