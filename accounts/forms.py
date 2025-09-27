from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )
    mpesa_phone_number = forms.CharField(
        max_length=15,
        label="M-Pesa Phone Number",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "2547XXXXXXXX"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove username field completely
        self.fields.pop("username", None)

        # Update placeholders
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password"}
        )
        self.fields["email"].widget.attrs.update({"placeholder": "Email Address"})

    def save(self, request):
        """Save user with first/last names, M-Pesa phone, and username=email"""
        user = super().save(request)

        # Force username = email
        user.username = user.email
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.save()

        # Attach M-Pesa phone number to Profile (extended model)
        from accounts.models import Profile

        profile, created = Profile.objects.get_or_create(user=user)
        profile.mpesa_phone_number = self.cleaned_data.get("mpesa_phone_number", "")
        profile.save()

        # Ensure email exists and is primary
        try:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={"verified": False, "primary": True},
            )
            if not email_address.primary:
                email_address.primary = True
                email_address.save()
        except Exception:
            # Fail silently if email record can't be created
            pass

        return user
