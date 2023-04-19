from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('django.contrib.auth.urls')),
    path('',include('pos_api.urls')),
]
admin.site.index_title = "TapNyamoo"
admin.site.site_header = "Cashless Administration"
admin.site.site_title = "Cashless"


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
