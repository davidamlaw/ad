from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User, Profile

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name')

    fieldsets = (
        ('User Information', {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin',)}),
        ('Date Joined', {'fields': ('date_joined',)}),
    )


admin.site.unregister(Group)
admin.site.register(User, MyUserAdmin)
admin.site.register(Profile)
