import requests #type: ignore
from django.conf import settings #type: ignore
from django.contrib.auth import get_user_model #type: ignore
from rest_framework.views import APIView #type: ignore
from rest_framework.generics import GenericAPIView #type: ignore
from rest_framework.response import Response    #type: ignore
from rest_framework import status #type: ignore
from rest_framework.permissions import AllowAny #type: ignore
from rest_framework_simplejwt.tokens import RefreshToken    #type: ignore
from google.oauth2 import id_token #type: ignore
from google.auth.transport import requests as google_requests #type: ignore
import jwt #type: ignore
import time
from .serializers import GoogleLoginSerializer

User = get_user_model()


class GoogleLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleLoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            email = idinfo['email']
            full_name = idinfo.get('name', '')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(email=email, full_name=full_name, is_active=True)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    