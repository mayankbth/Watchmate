from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
# "obtain_auth_token" will give us access to token if we send our user name and password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_app.api.views import registration_view, logout_view


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # # this is for JWT authentication system.
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]