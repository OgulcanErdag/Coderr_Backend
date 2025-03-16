from django.core.management.base import BaseCommand
from order_app.models import Order

class Command(BaseCommand):
    help = "Löscht kaputte oder ungültige Bestellungen"

    def handle(self, *args, **kwargs):
        fail_orders = Order.objects.filter(
        business_user__username__in=["andrey", "kevin"]
    ).filter(
        customer_user__isnull=True
    ) | Order.objects.filter(
        customer_user__username__in=["andrey", "kevin"],
        business_user__isnull=True
    )
        total = fail_orders.count()

        if total > 0:
            self.stdout.write(self.style.WARNING(f"{total} kaputte Bestellungen gefunden."))
            fail_orders.delete()
            self.stdout.write(self.style.SUCCESS("✅ Kaputte Bestellungen erfolgreich gelöscht."))
        else:
            self.stdout.write("👍 Keine kaputten Bestellungen gefunden.")
