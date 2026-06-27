from django.test import TestCase

from order.factories import OrderFactory
from order.models import Order
from order.serializers import OrderSerializer
from product.factories import ProductFactory, UserFactory


class OrderSerializerTestCase(TestCase):
    def test_serialize_order_computes_total(self):
        user = UserFactory()
        product_a = ProductFactory(price=20)
        product_b = ProductFactory(price=30)
        order = OrderFactory(user=user, product=[product_a, product_b])

        data = OrderSerializer(order).data

        self.assertEqual(data["user"], user.id)
        self.assertEqual(len(data["product"]), 2)
        self.assertEqual(data["total"], 50)

    def test_serialize_order_treats_null_prices_as_zero(self):
        user = UserFactory()
        product_with_price = ProductFactory(price=15)
        product_without_price = ProductFactory(price=None)
        order = OrderFactory(
            user=user,
            product=[product_with_price, product_without_price],
        )

        data = OrderSerializer(order).data

        self.assertEqual(data["total"], 15)

    def test_serialize_order_with_no_products(self):
        order = OrderFactory(product=[])

        data = OrderSerializer(order).data

        self.assertEqual(data["product"], [])
        self.assertEqual(data["total"], 0)

    def test_create_order_with_nested_products(self):
        user = UserFactory()
        payload = {
            "user": user.id,
            "product": [
                {
                    "title": "Order Book",
                    "description": "Included in order",
                    "price": 40,
                    "active": True,
                    "category": [
                        {
                            "title": "Drama",
                            "slug": "drama",
                            "description": "Drama books",
                            "active": True,
                        }
                    ],
                }
            ],
        }

        serializer = OrderSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()

        self.assertIsInstance(order, Order)
        self.assertEqual(order.user, user)
        self.assertEqual(order.product.count(), 1)
        self.assertEqual(order.product.first().title, "Order Book")
