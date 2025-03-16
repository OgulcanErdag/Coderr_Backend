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
            errors["revisions"] = ["Revisionen hoher als 1 oder Unbegrenzt."]
        if delivery_time_in_days is not None and delivery_time_in_days <= 0:
            errors["delivery_time_in_days"] = ["Lieferzeit muss mindestens 1 Tag sein."]
        if not features or len(features) == 0:
            errors["features"] = ["Mindestens eine feature muss vorhanden sein."]
        if price is not None and price <= 0:
            errors["price"] = ["Preis muss hoher als 1 sein."]
        return errors

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        
        details_data = validated_data.pop('details', [])
        request = self.context.get('request')  
        user = request.user  
        offer = Offer.objects.create(user=user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def validate(self, data):
        
        details = data.get('details', None)
        if details is not None: 
            if len(details) != 3:
                raise serializers.ValidationError("Exactly three details (basic, standard, premium) are required.")
            offer_types = [detail['offer_type'] for detail in details]
            if len(set(offer_types)) != 3 or not all(offer_type in ['basic', 'standard', 'premium'] for offer_type in offer_types):
                raise serializers.ValidationError("Details must include exactly one of each: basic, standard, premium.")
        return data

    def update(self, instance, validated_data):
        
        details_data = validated_data.pop('details', None)  
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

