from django.urls import path
from accounts import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("profile/", views.profile, name="profile"),
    path(
        "password/change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path("delete/", views.delete_user, name="delete_user"),
    path("delete/confirm/", views.confirm_delete, name="confirm_delete_user"),
    path(
        "verify/<str:email>/<uuid:code>/",
        views.email_verification_view,
        name="email_verification",
    ),
    path(
        "verify/resend/",
        views.resend_email_verification_view,
        name="resend_email_verification",
    ),
    path("email/change/", views.change_email, name="change_email"),
    path("password/reset/email/", views.reset_password_email, name='password_reset_email'),
    path('password/reset/<str:email>/<uuid:code>/', views.reset_password, name='password_reset')
    
]
