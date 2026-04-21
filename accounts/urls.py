from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.views import AccountViewSet, AccountUpdateView, RegisterView
from .views import RegisterView

urlpatterns = [
    path('info/', AccountViewSet.as_view(), name='user_info'),
    path('update', AccountUpdateView.as_view(), name='update_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
]
