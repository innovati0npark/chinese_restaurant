from django.db import models
from seller.models import Food
from django.contrib.auth.models import User
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.DO_NOTHING)
    amount = models.IntegerField(default=0)

class CartItem(models.Model):
    product = models.ForeignKey(Food, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product