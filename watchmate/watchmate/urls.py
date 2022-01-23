from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('movies/', include('watchlist_app.api.urls'))
    path('watch/', include('watchlist_app.api.urls')),
    path('account/', include('user_app.api.urls')),

    # Temporary Login and Logout
    # path('api-auth/', include('rest_framework.urls')),
    # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    # this is going to give us temporary login form.
]
