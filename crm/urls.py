from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import admin
from django.urls import path,include
from leads.views import LandingPageView,SignupView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view() , name = "home"),
    path("leads/" , include("leads.urls" )),
    path("agents/" , include("agents.urls" )),
    path("login/" , LoginView.as_view(),name = "login"),
    path("logout/" , LogoutView.as_view(),name = "logout"),
    path("signup/" , SignupView.as_view(),name = "signup"),

    path("reset-password/" , PasswordResetView.as_view(),name = "reset_password"),
    path("password-reset-done/" , PasswordResetDoneView.as_view(),name = "password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/" , PasswordResetConfirmView.as_view(),name = "password_reset_confirm"),
    path("password-reset-complete/" , PasswordResetCompleteView.as_view(),name = "password_reset_complete"),
]

# urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()