from django.contrib import admin
from .models import Offer, OfferDetail

class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0


class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'preview_image', 'created_at']
    readonly_fields = ['preview_image']
    inlines = [OfferDetailInline]

    def preview_image(self, obj):
        if obj.image:
            return obj.image.url
        return "(Kein Bild)"
    preview_image.allow_tags = True
    preview_image.short_description = "Vorschau"


class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer', 'price', 'delivery_time_in_days', 'offer_type']
    list_filter = ['offer_type']
    search_fields = ['title', 'offer__title']


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
