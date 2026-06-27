from rest_framework import serializers

from order.models import Order
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        return sum(product.price or 0 for product in instance.product.all())

    class Meta:
        model = Order
        fields = ["user", "product", "total"]

    def create(self, validated_data):
        products_data = validated_data.pop("product")
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            product = ProductSerializer().create(product_data)
            order.product.add(product)
        return order
