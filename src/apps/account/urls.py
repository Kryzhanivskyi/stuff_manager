from django.urls import path

from apps.account.views import index, profile, contact_us, create_request

app_name = "account"

urlpatterns = [
    path("index/", index),
    path("profile/", profile, name="profile"),
    path("contact-us/", contact_us),
    path('create-request/', create_request, name='create-request')
]