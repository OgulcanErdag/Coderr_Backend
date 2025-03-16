from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'customer_user',
        'business_user',
        'offer_type',
        'status',
        'created_at',
    )
    list_filter = ('status', 'offer_type', 'created_at')
    list_display = ( "title", "revisions", "status")
    search_fields = ('title', 'customer_user__username', 'business_user__username')
