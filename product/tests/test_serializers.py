from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer


class CategorySerializerTestCase(TestCase):
    def test_serialize_category(self):
        category = CategoryFactory(
            title="Fiction",
            slug="fiction",
            description="Fiction books",
            active=True,
        )

        data = CategorySerializer(category).data

        self.assertEqual(data["title"], "Fiction")
        self.assertEqual(data["slug"], "fiction")
        self.assertEqual(data["description"], "Fiction books")
        self.assertTrue(data["active"])

    def test_create_category(self):
        payload = {
            "title": "Science",
            "slug": "science",
            "description": "Science books",
            "active": True,
        }

        serializer = CategorySerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()

        self.assertIsInstance(category, Category)
        self.assertEqual(Category.objects.count(), 1)


class ProductSerializerTestCase(TestCase):
    def test_serialize_product_with_categories(self):
        category = CategoryFactory(title="Horror", slug="horror")
        product = ProductFactory(title="Dracula", price=50)
        product.category.add(category)

        data = ProductSerializer(product).data

        self.assertEqual(data["title"], "Dracula")
        self.assertEqual(data["price"], 50)
        self.assertTrue(data["active"])
        self.assertEqual(len(data["category"]), 1)
        self.assertEqual(data["category"][0]["title"], "Horror")
        self.assertEqual(data["category"][0]["slug"], "horror")

    def test_create_product_with_categories(self):
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

        serializer = ProductSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()

        self.assertIsInstance(product, Product)
        self.assertEqual(product.title, "New Book")
        self.assertEqual(product.category.count(), 1)
        self.assertEqual(product.category.first().slug, "fantasy")
