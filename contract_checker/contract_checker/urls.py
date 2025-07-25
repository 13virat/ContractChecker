from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comparison.urls')),  # Default page
    path('accounts/', include('allauth.urls')),
]
