from django.urls import path

from gym.views import GymListCreateAPIView, SportTypeListCreateAPIView, LocationListCreateAPIView, GymDetailAPIView

urlpatterns = [
    path('gym-list/', GymListCreateAPIView.as_view(), name='gym-list'),
    path('sport-type/', SportTypeListCreateAPIView.as_view(), name='sport-type'),
    path('location-list/', LocationListCreateAPIView.as_view(), name='location-list'),
    path('gym-detail/<uuid:id>/', GymDetailAPIView.as_view(), name='gym-detail'),    
]