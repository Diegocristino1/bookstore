import factory

from order.models import Order
from product.factories import ProductFactory, UserFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted is not None:
            for item in extracted:
                self.product.add(item)
        else:
            self.product.add(ProductFactory())
