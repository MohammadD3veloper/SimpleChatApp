from django.urls import path
from .views import (
    login,
    logout,
    dashboard,
    send_code,
    UserUpdateView
)


app_name = "user"

urlpatterns = [
    path("", login, name="login"),
    path("logout/", logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path('update/<int:pk>/', UserUpdateView.as_view(), name="update"),
    path("ajax/code/", send_code, name="send_code")
]