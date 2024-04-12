from django.urls import path

from .views import login_user, logout_user, register_user
from .views import (
    SignUpView, ActivateView, CheckEmailView, SuccessView
)

urlpatterns = [
    path('login_user/', login_user, name='login'),
    path('logout_user/', logout_user, name='logout'),
    path('register_user/', register_user, name='register'),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name="activate"),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('success/', SuccessView.as_view(), name="success"),
]
