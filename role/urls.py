from django.urls import path

from role.views import CreateUserView, AllUsersListView, OwnerListCreateAPIView, TrainerListCreateAPIView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('users/all/', AllUsersListView.as_view(), name='all-users-list'),
    path('owners/list/create', OwnerListCreateAPIView.as_view(), name='owner-list-create'),
    path('trainers/list/create', TrainerListCreateAPIView.as_view(), name='trainer-list')
]
