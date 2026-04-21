from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

from . import serializers
from accounts import models

from django.http import FileResponse, Http404
from django.conf import settings

from rest_framework.decorators import api_view

import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
import uuid, base64

from .models import User
from .serializers import RegisterSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class AccountViewSet(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if not self.request.user.is_authenticated:
            return models.User.objects.none()

        return self.request.user


class AccountUpdateView(generics.UpdateAPIView):
    """
    error: old_and_new_password_id_required_for_change_password, owner_cannot_change_password, old_password_id_wrong
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.AccountUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if not self.request.user.is_authenticated:
            return models.User.objects.none()

        return self.request.user

    def update(self, request, *args, **kwargs):
        new_pass = request.data.get('new_password', None)
        old_pass = request.data.get('old_password', None)

        if (new_pass and not old_pass) or (not new_pass and old_pass):
            return Response({"detail": "old_and_new_password_id_required_for_change_password"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user

        if new_pass and old_pass:
            if user.type == 'owner':
                return Response({"detail": "owner_cannot_change_password"}, status=status.HTTP_400_BAD_REQUEST)
            elif check_password(old_pass, user.password):
                user.set_password(new_pass)
                user.save()
            else:
                return Response({"detail": "old_password_id_wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


@api_view(["GET"])
def serve_image(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, "media/", filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), content_type="image/*")
    else:
        raise Http404("Image not found")


@api_view(['POST'])
def cleare_data(request, phone_number):
    from django.apps import apps
    from accounts.models import User

    for model in apps.get_models():
        for field in model._meta.get_fields():
            if field.is_relation and getattr(field, 'related_model', None) == User:
                print(type(model))
                print(f"{model.__name__}.{field.name}")

    return Response('success')


class DeleteAccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.type == 'owner':
            for worker in models.User.objects.all():
                if worker.boss == user:
                    worker.state = -1
                    worker.save()
        user.state = -1
        user.save()
        return Response({"detail": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(["POST"])
def save_image(request):
    try:
        data = request.data
        image_base64 = data.get("image")
        file_type = data.get("file_type", 'png')

        if not image_base64:
            return JsonResponse({"error": "Image is required"}, status=400)

        if file_type not in ["gif", "png", "mp4"]:
            return JsonResponse({"error": "Invalid file type"}, status=400)

        image_uuid = str(uuid.uuid4())
        filename = f"{image_uuid}.{file_type}"

        save_path = os.path.join(settings.MEDIA_ROOT, "images/")
        os.makedirs(save_path, exist_ok=True)

        try:
            file_data = base64.b64decode(image_base64)
        except Exception as e:
            return JsonResponse({"error": f"Base64 decoding error: {e}"}, status=400)

        file_path = os.path.join(save_path, filename)

        with open(file_path, "wb") as f:
            f.write(file_data)

        return JsonResponse({"message": "File saved successfully", "file_name": filename.split('.')[0]}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


