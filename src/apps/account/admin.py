from django.contrib import admin
from apps.account.models import User


@admin.register(User)
class HeroAdmin(admin.ModelAdmin):
    readonly_fields = ["username", "last_login", "date_joined", "password"]