from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr

from app.config import settings

env = Environment(loader=FileSystemLoader("app/templates"))


def template_email_conformation_booking(
        bookings: list,
        email_to: EmailStr
):
    template = env.get_template('email_confirm_booking.html')

    email = EmailMessage()
    email['Subject'] = 'Подтверждение бронирования'
    email['From'] = settings.SMTP_EMAIL
    email['To'] = email_to

    context = {"bookings": bookings}

    email.set_content(template.render(**context), subtype="html")

    return email
