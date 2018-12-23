from django.urls import path

from apps.account.views import index

urlpatterns = [
    path("index/", index)
]