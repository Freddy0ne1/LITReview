from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
    path("__reload__/", include("django_browser_reload.urls")),

]

# Configuration pour servir les fichiers média en mode développement
# IMPORTANT : Ceci ne fonctionne que quand DEBUG = True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)