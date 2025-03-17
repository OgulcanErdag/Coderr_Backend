from django.urls import path
from .views import ReviewListView, ReviewDetailsView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name="review-list"),
    path('reviews/<int:pk>/', ReviewDetailsView.as_view(), name="review-details"),
]
