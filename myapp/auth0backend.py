from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings
from jose import jwt
from auth0.authentication import GetToken
from auth0.management import Auth0


class Auth0Backend(BaseBackend):
    def authenticate(self, request, token=None):
        if token:
            try:
                payload = jwt.decode(
                    token,
                    settings.AUTH0_CLIENT_SECRET,
                    audience=settings.AUTH0_CLIENT_ID,
                    algorithms=['HS256']
                )
            except jwt.ExpiredSignatureError:
                return None

            user_id = payload.get('sub')
            if user_id:
                access_token = self.get_management_api_token()
                user_info = self.get_user_info(access_token, user_id)
                user, _ = User.objects.get_or_create(username=user_info['email'])
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_management_api_token(self):
        client_id = settings.AUTH0_CLIENT_ID
        client_secret = settings.AUTH0_CLIENT_SECRET
        domain = settings.AUTH0_DOMAIN

        get_token = GetToken(domain)
        token = get_token.client_credentials(client_id, client_secret, f'https://{domain}/api/v2/')
        return token['access_token']

    def get_user_info(self, access_token, user_id):
        domain = settings.AUTH0_DOMAIN
        auth0 = Auth0(domain, access_token)
        user_info = auth0.users.get(user_id)
        return user_info

        