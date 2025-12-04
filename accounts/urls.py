from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MeView, RegisterView
from .token_views import EmailTokenObtainPairView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("token/", EmailTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
]
