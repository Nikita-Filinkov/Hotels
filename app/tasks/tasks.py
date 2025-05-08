from pydantic import EmailStr

from app.tasks.celery_connection import celery
from PIL import Image
from pathlib import Path
from app.tasks.email.email_templates import template_email_conformation_booking
import smtplib
from app.config import settings


@celery.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resize_1000_500 = im.resize((1000, 500))
    im_resize_200_100 = im.resize((200, 100))
    im_resize_1000_500.save(f'app/static/images/resized_{im_path.name}')
    im_resize_200_100.save(f'app/static/images/resized_{im_path.name}')


@celery.task
def send_email_conformation_booking(
        bookings: list,
        email_to: EmailStr
):
    message = template_email_conformation_booking(bookings, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASS)
        server.send_message(message)
