from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'type', 'team')


class AdminUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'type', 'team', 'is_active', 'is_staff')

    def validate(self, attrs):
        if self.instance and self.instance.is_superuser:
            raise serializers.ValidationError('Cannot update superuser')

        if attrs.get('team') and attrs.get('is_staff'):
            raise serializers.ValidationError('Leave team field empty for staff users')
        return attrs

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('User already exists')

        user = User.objects.create_user(**validated_data, is_active=False, username=validated_data['email'])
        return user


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'password')
        lookup_field = 'id'

    # @todo: add password validation

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


__all__ = [
    'UserSerializer',
    'AdminUserSerializer',
    'ChangePasswordSerializer'
]
