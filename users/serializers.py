from typing import Any

from django.contrib.auth import get_user_model


from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from users.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)

from users.models import Pharmacist

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = ("id", "email", "username", "password")

    def create(self, validated_data: Any) -> Any:
        user = User.objects.create_user(**validated_data)
        user.save()

        return user


class PharmacistSerializer(serializers.ModelSerializer):
    """
    Employee serializer
    """
    id = serializers.CharField(
        read_only=True
    )
    pharmacist = UserSerializer(read_only=True)
    first_name = serializers.CharField(min_length=2, max_length=90)
    last_name = serializers.CharField(min_length=2, max_length=90)
    contact = serializers.IntegerField()
    employee_number = serializers.CharField(min_length=2, max_length=40)

    class Meta:
        model = Pharmacist
        fields = (
            "id",
            "pharmacist",
            "first_name",
            'last_name',
            'contact',
            'employee_number',
        )

        read_only_fields = (
            'id',
            'pharmacist'
        )

    def create(self, validated_data):
        """
        set current user as pharmacist
        """
        validated_data['pharmacist'] = self.context.get("request").user
        employee = super().create(validated_data)
        return employee
