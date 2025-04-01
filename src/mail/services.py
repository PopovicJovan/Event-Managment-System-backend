from src.mail.utils import send_registration_email
from src.users.models import User

def send_welcome_email(user: User):
    send_registration_email(recipient=user)