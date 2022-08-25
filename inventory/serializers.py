from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from inventory.models import Inventory, CartItem, Order
from users.models import Manufacturer
from users.serializers import UserSerializer

class InventorySerializer(serializers.ModelSerializer):
    """
    Inventory model serializer
    """
    id = serializers.CharField(read_only=True)
    item_name = serializers.CharField(min_length=2, max_length=255)
    item_description = serializers.CharField(min_length=2, max_length=255)
    item_type = serializers.CharField(min_length=2, max_length=90)
    item_code = serializers.CharField(
        min_length=2,
        max_length=15,
        validators=[UniqueValidator(queryset=Inventory.objects.all())]
    )
    item_price = serializers.IntegerField(default=1)
    expiry = serializers.DateField()
    quantity_in = serializers.IntegerField()
    distributor = serializers.SlugRelatedField(
        queryset=Manufacturer.objects.all(), slug_field="company_name"
    )
    entered_by = UserSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = (
            'id',
            'item_name',
            'item_description',
            'item_type',
            'item_code',
            'item_price',
            'expiry',
            'quantity_in',
            "distributor",
            'entered_by',
            'created_at',
        )

        read_only_fields = (
            'id',
            'created_at',
            'entered_by',
        )

    def create(self, validated_data):
        ''''''
        request = self.context["request"]
        validated_data["entered_by"] = request.user
        instance = Inventory.objects.create(**validated_data)
        return instance


class CartSerializer(serializers.ModelSerializer):
    """
    Cart serializer
    """
    id = serializers.CharField(read_only=True)
    product = serializers.SlugRelatedField(
        queryset=Inventory.objects.all(), slug_field="item_name"
    )
    user = UserSerializer(read_only=True)
    product_quantity = serializers.IntegerField()
    total = serializers.FloatField(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'product',
            'user',
            'product_quantity',
            'total',
            'created_at',
        )
        read_only_fields = (
            'id',
            'total',
            'created_at',
            'user'
        )

    def create(self, validated_data):
        """"""
        request = self.context['request']
        validated_data['user'] = request.user
        instance, _ = CartItem.objects.get_or_create(**validated_data)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    """"""
    id = serializers.CharField(read_only=True)
    product = serializers.SlugRelatedField(
        queryset=Inventory.objects.all(), slug_field="item_code"
    )
    customer_name = serializers.CharField(
        min_length=2,
        max_length=90
    )
    product_quantity = serializers.IntegerField()
    product_price = serializers.FloatField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)
    served_by = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "product",
            "customer_name",
            "product_quantity",
            "product_price",
            "total_amount",
            "served_by",
        )
        read_only_fields = (
            "id",
            "product_price",
            "total_amount",
            "created_at",
            "served_by",
        )

    def create(self, validated_data):
        """"""
        request = self.context['request']
        validated_data['served_by'] = request.user
        instance = Order.objects.create(**validated_data)
        return instance

