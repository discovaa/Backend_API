from .serializers import RegistrationSerializer, VerifyOTPSerializer, MyTokenObtainPairSerializer
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth_api.models import User
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegistrationAPIView(generics.GenericAPIView):
    '''Registers user'''
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = {}
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            data['response'] = "Registration Successful!"
            refresh = RefreshToken.for_user(user=user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

        return Response(data, status.HTTP_201_CREATED)

class VerifyOTPAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            otp = serializer.data['otp']
            user_obj = User.objects.get(email=email)
            
            if user_obj.otp == otp:
                user_obj.is_staff = True
                user_obj.save()
                return Response("verified")
            return Response(serializer.data,status.HTTP_400_BAD_REQUEST)


class LogoutBlacklistTokenUpdateView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
class DemoView(APIView):
    # authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    
    def post(self,request):
        try:
            return Response("accessed")
        except Exception as e:
            print(e)
            return Response("")
class DemoView2(APIView):
    # authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            return Response("accessed 2")
        except Exception as e:
            print(e)
            return Response("")