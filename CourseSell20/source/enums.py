from django.db import models


class Role(models.TextChoices):
    admin = "admin", "Администратор"
    staff = "seller", "Продавец"
    user = "user", "Пользователь"
