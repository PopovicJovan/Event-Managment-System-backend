import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth


load_dotenv()

class AuthSettings:
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET')

auth_settings = AuthSettings()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=auth_settings.GOOGLE_CLIENT_ID,
    client_secret=auth_settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    refresh_token_url=None,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)
