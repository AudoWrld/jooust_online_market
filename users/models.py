from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, second_name, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not second_name:
            raise ValueError("Users must have a second name")

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, second_name=second_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, second_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email, first_name, second_name, password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    second_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=60, unique=True, null=False, blank=False)
    mpesa_phone_number = models.CharField(
        max_length=15, unique=True, null=True, blank=True
    )
    email_verified = models.BooleanField(default=False)

    # required fields for admin and auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "second_name"]

    def __str__(self):
        return f"{self.first_name} {self.second_name} <{self.email}>"


class DeliveryArea(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="delivery_areas",
    )
    area = models.CharField(max_length=100, help_text="Gate A, Gate B")
    hostel_name = models.CharField(
        max_length=100, help_text="Sunshine, Manhattan, Waridi"
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hostel_name} - {self.area} ({'Active' if self.is_active else 'Inactive'})"

    def save(self, *args, **kwargs):
        # if this delivery area is being set as active,
        # deactivate all other areas for this user
        if self.is_active:
            DeliveryArea.objects.filter(user=self.user, is_active=True).update(
                is_active=False
            )
        super().save(*args, **kwargs)
