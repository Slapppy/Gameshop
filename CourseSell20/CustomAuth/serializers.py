from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from source.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
