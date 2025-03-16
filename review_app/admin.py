from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_user', 'reviewer', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'business_user', 'reviewer', 'created_at')
    search_fields = ('description', 'business_user__username', 'reviewer__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

   
