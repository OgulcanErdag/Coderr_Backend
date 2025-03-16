from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'tel', 'location', 'created_at', 'profile_pic_preview')
    list_filter = ('type', 'created_at')
    search_fields = ('user__username', 'tel', 'location')

    def profile_pic_preview(self, obj):
        if obj.file:
            return format_html(obj.file.url)
        return "Kein Bild"
    
    profile_pic_preview.short_description = "Profilbild"

admin.site.register(UserProfile, UserProfileAdmin)
