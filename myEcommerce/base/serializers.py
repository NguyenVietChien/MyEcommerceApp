# import serializers from the REST framework
from rest_framework import serializers

# import the todo data model
from .models import Product

# create a serializer class


class TodoSerializer(serializers.ModelSerializer):

    # create a meta class
    class Meta:
        model = Product
        fields = ('product_name', 'product_price',
                  'product_link', 'rating_point', 'total_comments')
