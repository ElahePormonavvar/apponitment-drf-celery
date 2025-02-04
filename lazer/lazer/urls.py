from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# --------------------------------------------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls',namespace='accounts')),
    path('appointments/', include('apps.appointments.urls',namespace='appointments')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
