import factory
from django.contrib.auth.models import User

from product.models import Category, Product


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")
    description = factory.Faker("sentence")
    active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker("paragraph")
    price = factory.Sequence(lambda n: (n + 1) * 10)
    active = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cat in extracted:
                self.category.add(cat)
