from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from .models import User


@shared_task
def send_inactive_user_reminder():
    inactive_users = User.objects.filter(
        is_active=True, last_login__lte=timezone.now() - timedelta(days=7)
    )

    for user in inactive_users:
        subject = "Your last entry to the store was a long time ago"
        message = (
            f"Уважаемый {user.first_name},\n\n"
            f"You haven't visited our store for a long time. Please visit us again!"
        )
        from_email = "ax-marat@mail.com"
        to_email = [user.email]

        send_mail(subject, message, from_email, to_email)
