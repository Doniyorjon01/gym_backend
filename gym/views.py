from rest_framework import viewsets, permissions, generics
from .models import SportType
from .serializers import SportTypeSerializer
from rest_framework.permissions import AllowAny

class SportTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    permission_classes = [AllowAny]



from rest_framework import viewsets, permissions
from .models import Gym
from .serializers import GymSerializer

class GymListCreateAPIView(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LocationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    

class GymDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
        

