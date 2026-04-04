from django.urls import path

from .views import (
    DashboardGestorView,
    DashboardResponsavelView,
    DashboardRouterView,
    HomeView,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardRouterView.as_view(), name="dashboard_router"),
    path("dashboard/gestor/", DashboardGestorView.as_view(), name="dashboard_gestor"),
    path("dashboard/responsavel/", DashboardResponsavelView.as_view(), name="dashboard_responsavel"),
]

