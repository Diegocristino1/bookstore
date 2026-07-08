from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSetTestCase(APITestCase):
    def test_list_categories(self):
        CategoryFactory(title="Fiction", slug="fiction")
        CategoryFactory(title="Science", slug="science")

        response = self.client.get(
            reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_category(self):
        category = CategoryFactory(
            title="Horror",
            slug="horror",
            description="Horror books",
        )

        response = self.client.get(
            reverse("category-detail",
                    kwargs={"version": "v1", "pk": category.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Horror")
        self.assertEqual(response.data["slug"], "horror")
        self.assertEqual(response.data["description"], "Horror books")

    def test_create_category(self):
        payload = {
            "title": "Fantasy",
            "slug": "fantasy",
            "description": "Fantasy books",
            "active": True,
        }

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.data["slug"], "fantasy")

    def test_update_category(self):
        category = CategoryFactory(title="Old Title", slug="old-title")

        response = self.client.patch(
            reverse("category-detail",
                    kwargs={"version": "v1", "pk": category.pk}),
            {"title": "Updated Title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.title, "Updated Title")

    def test_delete_category(self):
        category = CategoryFactory()

        response = self.client.delete(
            reverse("category-detail",
                    kwargs={"version": "v1", "pk": category.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
