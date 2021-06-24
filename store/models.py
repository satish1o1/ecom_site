from django.db import models
from django.contrib.auth.models import User

# class Customer(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
#     name = models.CharField(max_length=50,null=True)

# def __str__(self):
#     return str(self.id)


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField(null=True)
    description = models.CharField(max_length=100,null=True)
    tage = models.CharField(max_length=30,null=True)
    image = models.ImageField()

    def __str__(self):
        return str(self.title)


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    statues = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=30, null=True)

    @property
    def get_cart_total(self):
        items = self.orderitems_set.all()
        return sum([item.get_item_total for item in items])

    @property
    def get_cart_items(self):
        items = self.orderitems_set.all()
        return sum([item.quantity for item in items])


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_item_total(self):
        return self.quantity * self.product.price


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
