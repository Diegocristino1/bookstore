from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.factories import OrderFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory, UserFactory


class OrderViewSetTestCase(APITestCase):
    def test_list_orders(self):
        OrderFactory()
        OrderFactory()

        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_order_computes_total(self):
        user = UserFactory()
        category = CategoryFactory()
        product_a = ProductFactory(price=20, category=[category])
        product_b = ProductFactory(price=30, category=[category])
        order = OrderFactory(user=user, product=[product_a, product_b])

        response = self.client.get(reverse("order-detail", kwargs={"pk": order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], user.id)
        self.assertEqual(len(response.data["product"]), 2)
        self.assertEqual(response.data["total"], 50)

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

        response = self.client.post(reverse("order-list"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, user)
        self.assertEqual(order.product.count(), 1)
        self.assertEqual(order.product.first().title, "Order Book")
        self.assertEqual(response.data["total"], 40)

    def test_delete_order(self):
        order = OrderFactory()

        response = self.client.delete(reverse("order-detail", kwargs={"pk": order.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
