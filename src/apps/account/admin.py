from django.contrib import admin
from apps.account.models import User


@admin.register(User)
class HeroAdmin(admin.ModelAdmin):
    readonly_fields = ["username", "last_login", "date_joined", "password", "phone_number"]
    list_display = ["id", "username", "age", "email"]
    list_filter = ["date_joined", "last_login", "age"]
    list_per_page = 10
    search_fields = ["email", "first_name", "phone_number"]

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return not obj.is_superuser
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.exclude(is_superuser=True)
        return qs