from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models, transaction
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email Address field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    phone = PhoneNumberField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            UserSetting.objects.get_or_create(user=self)


class UserSetting(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_settings"
    )
    notification_emails = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)

    def __str__(self):
        return f"User settings for '{self.user.email}'"
