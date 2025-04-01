from src.mail.config import mail_settings
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from jinja2 import Template
from src.users.models import User


conf = ConnectionConfig(
        MAIL_USERNAME=mail_settings.MAIL_USERNAME,
        MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
        MAIL_FROM=mail_settings.MAIL_FROM,
        MAIL_PORT=mail_settings.MAIL_PORT,
        MAIL_SERVER=mail_settings.MAIL_SERVER,
        MAIL_STARTTLS=mail_settings.MAIL_TLS,
        MAIL_SSL_TLS=mail_settings.MAIL_SSL,
        USE_CREDENTIALS=True,
        TEMPLATE_FOLDER='./src/templates/email/'
        )


def send_registration_email(recipient: User):
    with open("./src/templates/email/registration.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    template = Template(html_content)
    template = template.render({"user": recipient})
    message = MessageSchema(
        subject="Notification",
        recipients=[recipient.email],
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    fm.send_message(message)