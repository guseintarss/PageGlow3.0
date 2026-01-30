from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from PageGlow import settings
from main.views import page_not_found

from rest_framework.routers import DefaultRouter
from users.views import RuleViewSet

router = DefaultRouter()
router.register(r'rules', RuleViewSet, basename='rule')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("main.urls")),
    path('users/',include("users.urls", namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'

