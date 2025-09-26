from django.shortcuts import render


def register(request):
    return render(request, "users/register.html")


def verify_email(request):
    pass


def verification_sent(request):
    return render(request, "users/verification_sent.html")


def login(request):
    return render(request, "users/login.html")


def forgot_password(request):
    return render(request, "users/reset_password.html")


def reset_password(request):
    return render(request, "users/reset_password.html")
