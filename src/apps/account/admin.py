from django.contrib import admin
from apps.account.models import User, City, ContactUs, RequestDayOffs
from apps.account.forms import UserAdminForm, RequestDayOffAdminForm, RequestDayOffAdminAddForm
from apps import model_choices as mch


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

class RequestDayOffsInline(admin.TabularInline):
    model = RequestDayOffs
    show_change_link = True
    readonly_fields = ('from_date', 'to_date')
    # form = ...

    # def get_formset(self, request, obj=None, **kwargs):
    #     pass


@admin.register(User)
class HeroAdmin(admin.ModelAdmin):
    readonly_fields = []
    list_display = ["id", "username", "age", "email"]
    list_filter = ["date_joined", "last_login", "age"]
    list_per_page = 10
    search_fields = ["email", "first_name", "phone_number"]
    inlines = [RequestDayOffsInline]
    # form = UserAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ['username', 'last_login', 'date_joined', 'password']
        return []

    def get_form(self, request, obj=None, **kwargs):
        if obj is None: # create user "+add"
            return UserAdminForm
        else: # change existing user
            return super().get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return not obj.is_superuser
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.exclude(is_superuser=True)
        return qs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass


@admin.register(RequestDayOffs)
class RequestDayOffsAdmin(admin.ModelAdmin):
    list_filter = ('status', 'type')
    readonly_fields = ()
    # TODO add form
    # TODO subtract dayoffs or vacations on Form Approve

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(self, request)
        if obj is not None:
            readonly_fields += ('user', )
            # if request.user.is_hr:  # check if request user in group
            # if obj.status != mch.STATUS_PENDING and not request.user.is_superuser:  # allow superuser to change status field
            # if obj.status != mch.STATUS_PENDING:
            #     readonly_fields += ('status', )
                # readonly_fields = readonly_fields + ('status', )
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return RequestDayOffAdminAddForm
        else:
            return RequestDayOffAdminForm






