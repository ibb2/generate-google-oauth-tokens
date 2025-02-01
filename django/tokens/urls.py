from django.urls import path

from . import views

urlpatterns = [
    path("tokens", views.generate_oauth_tokens),
    path("tokens/refresh", views.refresh_access_token),
]
