from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-guest-user/', views.RegisterGuestUser.as_view()),
    path('users/user-info/<str:user_name>', views.UserInfo.as_view()),
    path('users/delete-user/<str:user_name>', views.UserDelete.as_view()),
]