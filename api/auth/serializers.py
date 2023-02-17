from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["username"],
        )
        
        return user
    
    class Meta:
        model = UserModel
        fields = ["email", "password", "username"]
        