from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.GetRoutes.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterUser.as_view()),
    path('users/list/', views.UserList.as_view()),
    path('users/user-info/<str:email>', views.UserInfo.as_view()),
    path('users/delete-user/<str:email>', views.UserDelete.as_view()),
]