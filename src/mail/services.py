from src.mail.utils import send_registration_email
from src.users.models import User

async def send_welcome_email(user: User):
    await send_registration_email(recipient=user)