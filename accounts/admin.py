from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User,Student,LibraryHistory,FeesHistory,Classes

class CustomUserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ('email', 'full_name', 'is_admin', 'is_staff', 'is_active')

    # Fields to filter in the admin list view
    list_filter = ('is_admin', 'is_staff', 'is_active')

    # Fieldsets for the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser','is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    # Fields used during the creation of a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2', 'is_admin', 'is_staff','is_superuser'),
        }),
    )

    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    # Add a method to handle `is_admin` for the admin list
    def is_admin(self, obj):
        return obj.is_admin
    is_admin.boolean = True  # Display as a boolean icon in the admin interface

# Register the custom user admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(LibraryHistory)
admin.site.register(FeesHistory)
admin.site.register(Classes)
