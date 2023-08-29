from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from .models import User

@shared_task
def send_inactive_user_reminder():
    # Найти пользователей, которые не заходили в магазин более 7 дней
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lte=timezone.now() - timedelta(seconds=20)
    )

    for user in inactive_users:
        # Отправить электронное письмо с напоминанием
        subject = "Предупреждение: Ваш последний вход в магазин был давно"
        message = f"Уважаемый {user.first_name},\n\n" \
                  f"Вы давно не заходили в наш магазин. Пожалуйста, посетите нас снова!"
        from_email = "ax-marat@mail.com"
        to_email = [user.email]

        send_mail(subject, message, from_email, to_email)
