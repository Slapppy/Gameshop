from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .enums import Role


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="source/static/source/images")
    release_date = models.DateField()


class Platform(models.Model):
    name = models.CharField(max_length=50)


class GamePlatform(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    balance = models.IntegerField(default=0)
    role = models.CharField(choices=Role.choices, max_length=15, default=Role.user)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()

    @property
    def is_superuser(self):
        return self.role == Role.admin

    @property
    def is_staff(self):
        return self.role in (Role.admin, Role.staff)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sum_order = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    review_datetime = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.first_name}'s Cart: {self.game.title} x{self.quantity}"
