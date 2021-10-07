from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('dj_rest_auth.urls')),
    # path('accounts/', include('allauth.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/book/', include('books.urls')),
]
