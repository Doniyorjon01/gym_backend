from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from role.serializers import CreateUserSerializer, UserDetailSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class AllUsersListView(generics.ListAPIView):
    queryset = User.objects.filter(state=1)
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


class OwnerListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(type='owner')
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    
class TrainerListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(type='trainer')
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        