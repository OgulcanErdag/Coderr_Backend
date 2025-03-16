from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from review_app.models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from order_app.models import Order

class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_permissions(self):
       
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user

        if not user.userprofile.type == 'customer':
            raise PermissionDenied("Nur Kunden können Bewertungen abgeben.")

        business_user = self.request.data.get("business_user")

        if not business_user:
            raise PermissionDenied("Kein Anbieter angegeben.")

        has_completed_order = Order.objects.filter(
            customer_user=user,
            business_user_id=business_user,
            status="completed"
        ).exists()

        if not has_completed_order:
            raise PermissionDenied("Du kannst nur bewerten, wenn du eine abgeschlossene Bestellung bei diesem Anbieter hast.")

        serializer.save(reviewer=user)

class ReviewDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
      
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
      
        if serializer.instance.reviewer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Nur der Ersteller oder ein Admin kann eine Bewertung bearbeiten.")
        serializer.save()

    def perform_destroy(self, instance):
    
        if instance.reviewer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Nur der Ersteller oder ein Admin kann eine Bewertung löschen.")
        instance.delete()

    def update(self, request, *args, **kwargs):
       
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)