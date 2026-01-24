from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from PageGlow import settings
from main.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("main.urls")),
    path('users/',include("users.urls", namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'

