from turtle import title
from django.db import models

# Create your models here.


class Product(models.Model):

    product_name = models.TextField(primary_key=True)
    product_price = models.IntegerField()
    product_link = models.TextField()
    rating_point = models.FloatField()
    total_comments = models.IntegerField()

    rating_5_star = models.IntegerField()
    rating_4_star = models.IntegerField()
    rating_3_star = models.IntegerField()
    rating_2_star = models.IntegerField()
    rating_1_star = models.IntegerField()

    platform = models.TextField()

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'myecommerce_tb'
