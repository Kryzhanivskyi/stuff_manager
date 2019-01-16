from django.contrib import admin
from django.urls import path, include
from apps.account.views import faq, tos

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("apps.account.urls", namespace="account")),
    path("faq/", faq),
    path("tos/", tos),
    path('accounts/', include('django.contrib.auth.urls')),
]
