from django.urls import path
from .views import RegistrationView, LoginView, UserProfileDetailView, BaseInfoView, BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
    path('profiles/business/', BusinessProfileListView.as_view(), name='business-profiles'),
    path('profiles/customer/', CustomerProfileListView.as_view(), name='customer-profiles'),
]
