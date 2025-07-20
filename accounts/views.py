from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, serializers  #
class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [ 'username', 'email']
        read_only_fields = ['id']

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for immediate login after registration
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get the user who just logged in
            user = User.objects.get(username=request.data['username'])
            user_data = UserSerializer(user).data
            
            # Add user data to the response
            response.data['user'] = user_data
            
            # Optionally set cookies for web access
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            
        return response

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Clear cookies if using cookie-based auth
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)