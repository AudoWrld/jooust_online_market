from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
