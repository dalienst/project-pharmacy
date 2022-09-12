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

from users.models import Pharmacist, Customer, Manufacturer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User model
    """

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
        Pharmacist.objects.create(pharmacist=user)

        return user


class PharmacistSerializer(serializers.ModelSerializer):
    """
    Employee serializer
    """
    id = serializers.CharField(
        read_only=True
    )
    username = serializers.CharField(read_only=True, source="pharmacist.username")
    first_name = serializers.CharField(min_length=2, max_length=90)
    last_name = serializers.CharField(min_length=2, max_length=90)
    contact = serializers.IntegerField()
    employee_number = serializers.CharField(min_length=2, max_length=40)

    class Meta:
        model = Pharmacist
        fields = (
            "id",
            "username",
            "first_name",
            'last_name',
            'contact',
            'employee_number',
        )

        read_only_fields = (
            'id',
            'pharmacist'
        )

    # def create(self, validated_data):
    #     """
    #     set current user as pharmacist
    #     """
    #     validated_data['pharmacist'] = self.context.get("request").user
    #     employee = super().create(validated_data)
    #     return employee

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.contact = validated_data.get("contact", instance.contact)
        instance.employee_number = validated_data.get("employee_number", instance.employee_number)
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer Model Serializer
    """
    id = serializers.CharField(
        read_only=True
    )
    customer = UserSerializer(
        read_only=True
    )
    first_name = serializers.CharField(min_length=2, max_length=90)
    last_name = serializers.CharField(min_length=2, max_length=90)
    contact = serializers.IntegerField()
    location = serializers.CharField(min_length=2, max_length=255)

    class Meta:
        model = Customer
        fields = (
            "id",
            "customer",
            "first_name",
            'last_name',
            'contact',
            "location",
        )

        read_only_fields = (
            'id',
            'customer'
        )

    def create(self, validated_data):
        """
        set current user as customer
        """
        validated_data['customer'] = self.context.get("request").user
        buyer = super().create(validated_data)
        return buyer

class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Manufacturer Model Serializer
    """
    id = serializers.CharField(
        read_only=True
    )
    manufacturer = UserSerializer(
        read_only=True
    )
    company_name = serializers.CharField(min_length=2, max_length=90)
    contact = serializers.IntegerField()
    location = serializers.CharField(min_length=2, max_length=255)
    license = serializers.CharField(
        min_length=2,
        max_length=255,
        validators=[UniqueValidator(queryset=Manufacturer.objects.all())],
    )


    class Meta:
        model = Manufacturer
        fields = (
            "id",
            "manufacturer",
            "company_name",
            'license',
            'contact',
            'location',
        )

        read_only_fields = (
            'id',
            'manufacturer'
        )

    def create(self, validated_data):
        """
        set current user as customer
        """
        validated_data['manufacturer'] = self.context.get("request").user
        distributor = super().create(validated_data)
        return distributor
