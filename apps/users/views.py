from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.utils import update_last_login


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            update_last_login(request)

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            update_last_login(request)

        return response
