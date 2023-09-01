from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('participant/', include('participants.urls')),
    path('preferences/', include('preferences.urls')),
    path('units/', include('units.urls')),
    path('games/', include('questions.urls')),
    path('', views.home, name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
