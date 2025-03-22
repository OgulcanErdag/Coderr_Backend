from rest_framework import serializers
from offer_app.models import Offer, OfferDetail

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = '__all__'

    def validate(self, data):
        errors = self._validate_fields(data)
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def _validate_fields(self, data):
        revisions = data.get('revisions')
        delivery_time_in_days = data.get('delivery_time_in_days')
        features = data.get('features')
        price = data.get('price')
        errors = {}
        if revisions is not None and revisions < -1:
            errors["revisions"] = ["Revisionen höher als 1 oder unbegrenzt (-1)."]
        if delivery_time_in_days is not None and delivery_time_in_days <= 0:
            errors["delivery_time_in_days"] = ["Lieferzeit muss mindestens 1 Tag sein."]
        if not features or len(features) == 0:
            errors["features"] = ["Mindestens eine Feature muss vorhanden sein."]
        if price is not None and price <= 0:
            errors["price"] = ["Preis muss höher als 1 sein."]
        return errors
class OfferSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    details = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['user']

    def get_details(self, obj):
        request = self.context.get('request')
        return [
            {
                "id": detail.id,
                "url": request.build_absolute_uri(f"/api/offerdetails/{detail.id}/") if request else f"/api/offerdetails/{detail.id}/"
            }
            for detail in obj.details.all()
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user  

        details_data = self.initial_data.get("details", [])
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def validate(self, data):
        details = self.initial_data.get("details", None)
        method = self.context.get("request").method if self.context.get("request") else None

        if method == "POST":
            if not details or len(details) != 3:
                raise serializers.ValidationError({
                    "non_field_errors": ["Exactly three details (basic, standard, premium) are required."]
                })
            offer_types = [d["offer_type"] for d in details]
            if len(set(offer_types)) != 3 or not all(typ in ["basic", "standard", "premium"] for typ in offer_types):
                raise serializers.ValidationError({
                    "non_field_errors": ["Details must include exactly one of each: basic, standard, premium."]
                })
        return data

    def update(self, instance, validated_data):
        details_data = self.initial_data.get("details", None)
        offer = super().update(instance, validated_data)

        if details_data is not None:
            offer.details.all().delete()
            for detail_data in details_data:
                detail_data.pop('offer', None)
                OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
class OfferTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = '__all__'
