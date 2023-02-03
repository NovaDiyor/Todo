from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.router import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('image/', include(router.url)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
