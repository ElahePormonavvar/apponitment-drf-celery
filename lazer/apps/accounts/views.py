from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,ActivateUserSerializer,SendActivationCodeSerializer,
                          ChangePasswordSerializer,CustomUserSerializer)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.accounts.models import CustomUser
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.utils import timezone

# ---------------------------------------------------------------------------------------------------------------
class RegisterUser(GenericAPIView):
    serializer_class = RegisterSerializer 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "کاربر با موفقیت ایجاد شد. کد فعال‌سازی به شماره موبایل شما ارسال شد."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ----------------------------------------------------------------------------------------------------------------
# class ActivateUser(APIView):
#     def post(self, request):
#         serializer = ActivateUserSerializer(data=request.data)
        
#         if serializer.is_valid():
#             data = serializer.save()
#             return Response(data, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUser(GenericAPIView):
    serializer_class = ActivateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # فعال‌سازی حساب کاربری
            user = serializer.save()

            # تولید توکن JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "حساب کاربری شما با موفقیت فعال شد. حالا می‌توانید وارد حساب خود شوید.",
                "refresh": str(refresh),
                "access": access_token,
                "user": {
                    "mobile_number": user.mobile_number,
                    "email": user.email,
                    "name": user.name,
                    "family": user.family,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        # به‌روزرسانی زمان آخرین ورود کاربر
        user.last_login = timezone.now()
        user.save()

        data.update({
            "message": "ورود با موفقیت انجام شد",
            "user": {
                "mobile_number": user.mobile_number,
                "email": user.email,
                "name": user.name,
                "family": user.family,
            }
        })
        return data

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# --------------------------------------------------------------------------------------
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "توکن رفرش ارائه نشده است"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)

            # دریافت `jti` که شناسه‌ی منحصربه‌فرد توکن است
            jti = token["jti"]

            # بررسی آیا توکن قبلاً در لیست بلک شده است یا نه
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                return Response({"error": "این توکن قبلاً بلاک شده است"}, status=status.HTTP_400_BAD_REQUEST)

            token.blacklist()  # بلاک کردن توکن
            return Response({"message": "با موفقیت خارج شدید"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"خطایی رخ داده است: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
# ------------------------------------------------------------------------------------------
class SendActivationCodeView(APIView):
    def post(self, request):
        serializer = SendActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کد فعال‌سازی به شماره موبایل ارسال شد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# --------------------------------------------------------------------------------------------        
class PasswordRememberRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کد فعال‌سازی ارسال شد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "رمز عبور با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]