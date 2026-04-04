from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("usuarios/", include("usuarios.urls")),
    path("turmas/", include("turmas.urls")),
    path("eventos/", include("eventos.urls")),
    path("avisos/", include("avisos.urls")),
]

