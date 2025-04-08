from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_205_RESET_CONTENT
from rest_framework.views import APIView, Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import Profile, PlanChoices

# Create your views here.
class JWTRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not email or not username:
            return Response({"error": "Email and username are required"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create the profile with default plan
        profile = Profile.objects.create(user=user, plan=PlanChoices.BASIC)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User registered successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

class JWTLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),

                "access": str(refresh.access_token)
            })

        return Response({"error": "Invalid credentials"}, status=400)

class JWTLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid or expired refresh token"}, status=HTTP_400_BAD_REQUEST)

class CheckUserPLan(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_plan = Profile.objects.get(user=request.user)
        return Response({"message": user_plan.get_plan_display()})

class CheckUserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = Profile.objects.create(user=request.user, plan=PlanChoices.BASIC)

        return Response({
            "email": request.user.email,
            "username": request.user.username,
            "plan": user_profile.get_plan_display()
        })
