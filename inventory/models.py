import math

from django.db import models
from users.abstracts import TimeStampedModel, UniversalIdModel
from users.models import Manufacturer
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save

User = get_user_model()


class Inventory(TimeStampedModel, UniversalIdModel):
    """
    Products entry model
    """
    # todo: add slug field
    item_name = models.CharField(max_length=255)
    item_description = models.CharField(max_length=255)
    item_type = models.CharField(max_length=90)
    item_price = models.FloatField(default=0)
    item_code = models.CharField(max_length=15)
    expiry = models.DateField(auto_now=False, auto_now_add=False, auto_created=False)
    quantity_in = models.BigIntegerField(default=0)
    distributor = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    entered_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name


class CartItem(TimeStampedModel, UniversalIdModel):
    """Items"""
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_quantity = models.BigIntegerField(default=1)
    # todo: total amount field
    total = models.FloatField(default=0)

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        """"""
        self.total = self.product.item_price * self.product_quantity
        return super().save(*args, **kwargs)


class Order(TimeStampedModel, UniversalIdModel):
    """
    This stores all orders made at the physical point of sale for users that do not use the API
    """
    # Todo: add unique order number or use the id as the unique number
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=500)
    product_quantity = models.PositiveIntegerField(default=1)
    served_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product_price = models.FloatField(default=0)
    total_amount = models.FloatField(blank=True,)
    # TODO: add payment mode in order model

    def save(self, *args, **kwargs):
        self.product_price = self.product.item_price * self.product_quantity
        self.total_amount = self.product_price
        return  super().save(*args, **kwargs)

# @receiver(pre_save, sender=Order)
# def total_amount_pre_save(sender, instance, **kwargs):
#     instance.total_amount = math.ceil(instance.total_amount * instance.product_quantity)


# class Checkout(TimeStampedModel, UniversalIdModel):
#     """"""
#     cart = models.ForeignKey(CartItem, on_delete=models.CASCADE)
