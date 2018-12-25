from django.urls import path
from apps.account.views import profile

urlpatterns = [
    path('profile/<id>/', profile),
]