from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout,authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from jose import jwt
from .auth0backend import Auth0Backend
from .utils import get_token


@csrf_exempt
def login(request):
    return redirect(f'https://{settings.AUTH0_DOMAIN}/authorize?'
                    f'audience={settings.AUTH0_AUDIENCE}&'
                    f'response_type=code&'
                    f'client_id={settings.AUTH0_CLIENT_ID}&'
                    f'redirect_uri=http://localhost:8000/callback/&'
                    f'scope=openid%20profile%20email&'
                    f'state=some-random-state')

@csrf_exempt
def callback(request):
    code = request.GET.get('code')
    if code:
        token =get_token(code)
        user = Auth0Backend.authenticate(request, token)
        if user:
            auth_login(request, user)
            return redirect('home')

    return redirect('login')

def logout(request):
    auth_logout(request)
    return redirect(f'https://{settings.AUTH0_DOMAIN}/v2/logout?'
                    f'returnTo=http://localhost:8000/&'
                    f'client_id={settings.AUTH0_CLIENT_ID}')

def home(request):
    return render(request, 'home.html')