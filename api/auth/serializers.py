from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserModel
        fields = ["email", "password", "username"]
    
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["username"],
        )
        
        return user

    def validate_password(self, value):
        min_length = 8
        if len(value) < 8:
            raise serializers.ValidationError(
                f"This password is too short. It must contain at least {min_length} character."
            )
            
        symbols = "~!@#$%^&*()_+{}\":;'[]"
        symbol_in_pwd = [char for char in value if char in symbols]
        if len(symbol_in_pwd) == 0:
            raise serializers.ValidationError(
                f"This password must contain at least 1 symbols. (symbols: {symbols})"
            )
        
        number_in_pwd = [char for char in value if char.isdecimal()]
        if len(number_in_pwd) == 0:
            raise serializers.ValidationError(
                f"This password must contain at least 1 numeric character."
            )
        