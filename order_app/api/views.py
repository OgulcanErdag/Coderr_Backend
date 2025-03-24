from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from order_app.models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from authentication_app.models import UserProfile
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
class OrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer  

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def perform_create(self, serializer):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("Kein UserProfile gefunden.")
        if profile.type != "customer":
            raise PermissionDenied("Nur Kunden können Bestellungen erstellen.")
        serializer.save()
class OrderStatusUpdateView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order = super().get_object()
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("Kein UserProfile gefunden.")
        if profile.type != "business":
            raise PermissionDenied("Nur Business-User dürfen den Bestellstatus aktualisieren.")
        return order
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
        full_data = OrderSerializer(instance, context={"request": request}).data
        return Response(full_data, status=status.HTTP_200_OK)
class OrderDeleteView(DestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]
class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
        
        order_count = Order.objects.filter(business_user=business_user, status="in_progress").count()
        return Response({"order_count": order_count}, status=200)  
class CompletedOrderCountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, business_user_id):
        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
        
        completed_order_count = Order.objects.filter(business_user=business_user, status="completed").count()
        return Response({"completed_order_count": completed_order_count}, status=200)