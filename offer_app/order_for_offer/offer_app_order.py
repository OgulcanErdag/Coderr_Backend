from django.db.models import QuerySet

class OrderingHelperOffers:
    ORDERING_OPTIONS = {
        "newest": "-created_at",
        "oldest": "created_at",
        "cheapest": "min_price",
        "expensive": "-min_price",
    }

    @staticmethod
    def apply_ordering(queryset: QuerySet, ordering: str) -> QuerySet:
        ordering_field = OrderingHelperOffers.ORDERING_OPTIONS.get(ordering, "-created_at")
        return queryset.order_by(ordering_field)
