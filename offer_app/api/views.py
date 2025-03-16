from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from offer_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferTypeSerializer
from .pagination import StandardResultsSetPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Min
from rest_framework.permissions import IsAuthenticated, AllowAny
from offer_app.order_for_offer.offer_app_order import OrderingHelperOffers

class OfferListView(ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        params = self.request.query_params

        offers = Offer.objects.annotate(min_price=Min('details__price'),min_delivery_time=Min('details__delivery_time_in_days'))

        if (creator_id := params.get('creator_id')):
            offers = offers.filter(user_id=creator_id)
        if (search := params.get('search', '')):
            offers = offers.filter(
                Q(title__icontains=search) | Q(description__icontains=search))
        if (max_delivery_time := params.get('max_delivery_time')):
            offers = offers.filter(details__delivery_time_in_days__lte=max_delivery_time)

        ordering = params.get('ordering')
        offers = OrderingHelperOffers.apply_ordering(offers, ordering)

        return offers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OfferDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferSerializer(offer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        offer = get_object_or_404(Offer, pk=pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OfferTypeDetailView(APIView):
    def get(self, request, pk, format=None):
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = OfferTypeSerializer(offer_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)                                                                                                                         


