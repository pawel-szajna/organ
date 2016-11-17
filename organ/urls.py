from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^manage/', admin.site.urls),
    url(r'^', include('organdb.urls')),
    url(r'^_nested_admin/', include('nested_admin.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
