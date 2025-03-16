from rest_framework import serializers
from review_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'business_user', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        
        reviewer = self.context['request'].user
        if not reviewer.is_authenticated:
            raise serializers.ValidationError({"detail": ["Sie müssen angemeldet sein, um eine Bewertung abzugeben."]})
        if 'reviewer' in self.initial_data and int(self.initial_data['reviewer']) != reviewer.id:
            raise serializers.ValidationError({"detail": ["Sie können keine Bewertung im Namen eines anderen Benutzers erstellen."]})
        business_user = data.get('business_user')
        if self.instance is None and Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError({"detail": ["Sie können nur eine Bewertung pro Geschäftsprofil abgeben."]})
        return data
    
    def create(self, validated_data):
        
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):

        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)