from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    google_avatar_url = models.URLField(blank=True, null=True)
    mpesa_phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        help_text="Enter your M-Pesa phone number (e.g., 2547XXXXXXXX).",
    )

    def __str__(self):
        return f"{self.user.email} Profile"
