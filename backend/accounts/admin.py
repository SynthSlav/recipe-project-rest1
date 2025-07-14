from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, ContactMessage


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["name", "email", "subject"]
    readonly_fields = ["created_at"]

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    mark_as_unread.short_description = "Mark selected messages as unread"
