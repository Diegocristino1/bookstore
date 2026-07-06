from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class ProductViewSetTestCase(APITestCase):
    def test_list_products(self):
        ProductFactory(title="Book A", price=20)
        ProductFactory(title="Book B", price=30)

        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_product_with_categories(self):
        category = CategoryFactory(title="Drama", slug="drama")
        product = ProductFactory(title="Hamlet", price=45)
        product.category.add(category)

        response = self.client.get(reverse("product-detail", kwargs={"pk": product.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Hamlet")
        self.assertEqual(response.data["price"], 45)
        self.assertEqual(len(response.data["category"]), 1)
        self.assertEqual(response.data["category"][0]["slug"], "drama")

    def test_create_product_with_nested_categories(self):
        payload = {
            "title": "New Book",
            "description": "A great read",
            "price": 35,
            "active": True,
            "category": [
                {
                    "title": "Fantasy",
                    "slug": "fantasy",
                    "description": "Fantasy books",
                    "active": True,
                }
            ],
        }

        response = self.client.post(reverse("product-list"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.title, "New Book")
        self.assertEqual(product.category.count(), 1)
        self.assertEqual(product.category.first().slug, "fantasy")

    def test_update_product(self):
        product = ProductFactory(title="Old Book", price=10)

        response = self.client.patch(
            reverse("product-detail", kwargs={"pk": product.pk}),
            {"price": 25},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.price, 25)

    def test_delete_product(self):
        product = ProductFactory()

        response = self.client.delete(reverse("product-detail", kwargs={"pk": product.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
