from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.exceptions import NotFound
from review_app.models import Review
from authentication_app.models import UserProfile
from offer_app.models import Offer 
from django.db.models import Avg

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key,"username": user.username,"email": user.email,"user_id": user.id}, 
                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"detail": f"Fehler bei der Registrierung: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user_id = self.kwargs['pk']
        try:
            return UserProfile.objects.get(user__id=user_id)  
        except UserProfile.DoesNotExist:
            raise NotFound("Kein passendes Profil gefunden.")

class BaseInfoView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(average_rating=Avg('rating'))['average_rating']
        average_rating = round(average_rating, 1) if average_rating is not None else 0
        business_profile_count = UserProfile.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data)
    
class BusinessProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_profiles = UserProfile.objects.filter(type="business")
        serializer = UserProfileSerializer(business_profiles, many=True)
        return Response(serializer.data)
    
class CustomerProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer_profiles = UserProfile.objects.filter(type="customer")
        serializer = UserProfileSerializer(customer_profiles, many=True)
        return Response(serializer.data)