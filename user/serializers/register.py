from rest_framework import serializers

from core.exceptions import APIError
from ..models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise APIError(detail='User already exists', code='USER_ALREADY_EXISTS')
        try:
            user = User(
                email=validated_data['email'],
                name=validated_data['name'],
                is_staff=validated_data['email'].endswith('@am.amrita.edu')
            )
            user.set_password(validated_data['password'])
            user.save()

        except Exception as e:
            raise APIError(detail=str(e), code='UNKNOWN_ERROR')

        return user

