import os
from dotenv import load_dotenv

load_dotenv()

class MailSettings:
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str  = os.getenv("MAIL_SERVER")
    MAIL_TLS: bool = os.getenv("TLS")
    MAIL_SSL: bool = os.getenv("SSL")

mail_settings = MailSettings()
