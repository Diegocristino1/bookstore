from rest_framework import serializers

from product.models import Product
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = ["title", "description", "price", "active", "category"]

    def create(self, validated_data):
        categories_data = validated_data.pop("category")
        product = Product.objects.create(**validated_data)
        for category_data in categories_data:
            category = CategorySerializer().create(category_data)
            product.category.add(category)
        return product