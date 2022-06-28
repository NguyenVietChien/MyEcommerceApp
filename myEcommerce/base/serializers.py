# import serializers from the REST framework
from rest_framework import serializers

# import the todo data model
from .models import Product

# create a serializer class


class TodoSerializer(serializers.ModelSerializer):

    # create a meta class
    class Meta:
        model = Product
        fields = '__all__'
