"""
Serializers for authentication.

Provides serializers for user authentication.
"""

from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    """Serializer for User objects."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "table",
            "deleted_at",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """Create a user with hashed password."""
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        """Update a user and hash the password if provided."""
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
