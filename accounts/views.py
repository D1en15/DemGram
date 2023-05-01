from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from accounts.models import User, EmailVerification, PasswordReset
from task_manager.celery import app
from accounts.forms import (
    LoginForm,
    RegistrationForm,
    PasswordChangeForm,
    EmailChangeForm,
    PasswordResetEmailForm,
    PasswordResetForm
)
from accounts.tasks import send_verification_email, send_password_reset_email


class LoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class PasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = PasswordChangeForm
    model = User
    success_url = reverse_lazy("accounts:logout")


class RegistrationView(CreateView):
    template_name = "accounts/registration.html"
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("homepage"))


@login_required
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    if not user.is_verified:
        return redirect(reverse("accounts:resend_email_verification"))
    else:
        user.delete()
        return redirect(reverse("accounts:logout"))


@login_required
def confirm_delete(request):
    return render(request, "accounts/confirm_delete_user.html")


@login_required
def profile(request, *args, **kwargs):
    user = User.objects.get(id=request.user.id)
    context = {"user": user}
    return render(request, "accounts/profile.html", context)


@login_required
def email_verification_view(request, email, code):
    user = User.objects.get(email=email, id=request.user.id)
    email_verification = get_object_or_404(EmailVerification, user=user, code=code)
    if not email_verification.is_expired():
        user.is_verified = True
        user.save()
        email_verification.delete()
        return render(request, "accounts/verification/verification_success.html")
    else:
        return render(request, "accounts/verification/verification_error.html")


@login_required
def resend_email_verification_view(request):
    user = User.objects.get(id=request.user.id)
    send_verification_email.delay(user.id)
    return render(request, "accounts/verification/verification_sended.html")


@login_required
def change_email(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            try:
                user.email = form.cleaned_data["email"]
                user.is_verified = False
                user.save()
                return redirect(reverse("accounts:resend_email_verification"))
            except:
                return render(request, "accounts/email_exists.html")
    else:
        form = EmailChangeForm(request.POST)
    return render(request, "accounts/email_change.html", {"form": form})


def reset_password_email(request):
    if request.method == "POST":
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            send_password_reset_email(user)
            return redirect(reverse("homepage"))
    else:
        form = PasswordResetEmailForm()

    return render(request, "accounts/password_reset_email.html", {"form": form})


def reset_password(request, email, code):
    user = User.objects.get(email=email)
    reset_password = get_object_or_404(PasswordReset, user=user, code=code)
    if not reset_password.is_expired():
        if request.method == 'POST':
            form = PasswordResetForm(user, request.POST)
            if form.is_valid():
                form.save(commit=True)
                reset = PasswordReset.objects.filter(user=user)
                reset.delete()
                return redirect(reverse('accounts:login'))
        else:
            form = PasswordResetForm(user)

    return render(request, 'accounts/password_reset.html', {'form' : form})