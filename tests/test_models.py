from django.test import TestCase
from restaurant.models import Menu

class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80)

        # Testing the str representation of the newly created Menu item
        self.assertEqual(str(item), "IceCream: $80.00")