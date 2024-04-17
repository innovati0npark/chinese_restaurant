from django.db import models
from django.contrib.auth.models import User             # 장고에서 만들어놓은 사용자 table
# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=200)

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #상품 판매자(user)
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.TextField()
    image_url = models.URLField()
    # Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    