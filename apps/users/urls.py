from django.urls import path

from .apps import UsersConfig
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
