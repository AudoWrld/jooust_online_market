from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin):
        """Create new user instance"""
        return User()

    def populate_user(self, request, sociallogin, data):
        """Populate user information from social provider data"""
        user = super().populate_user(request, sociallogin, data)

        email = data.get("email")
        if email:
            # Set email and username as the same
            user.email = email
            user.username = email

        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        return user

    def save_user(self, request, sociallogin, form=None):
        """Save user and create verified email address"""
        user = super().save_user(request, sociallogin, form)

        if user.email:
            # Always ensure username = email
            if not user.username:
                user.username = user.email
                user.save(update_fields=["username"])

            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={"verified": True, "primary": True},
            )
            if not email_address.verified or not email_address.primary:
                email_address.verified = True
                email_address.primary = True
                email_address.save()

        # Handle Google avatar URL
        if sociallogin.account.provider == "google":
            extra_data = sociallogin.account.extra_data
            google_avatar_url = extra_data.get("picture")
            if google_avatar_url:
                try:
                    from accounts.models import Profile

                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.google_avatar_url = google_avatar_url
                    profile.save(update_fields=["google_avatar_url"])
                except ImportError:
                    pass
                except Exception as e:
                    logger.warning(f"Failed to save Google avatar: {e}")

        return user

    def pre_social_login(self, request, sociallogin):
        """Handle existing users trying to connect social account"""
        if sociallogin.is_existing:
            return

        if sociallogin.user and sociallogin.user.email:
            try:
                existing_user = User.objects.get(email=sociallogin.user.email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass
