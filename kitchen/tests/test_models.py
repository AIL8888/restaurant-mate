from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.models import DishType, Dish


class DishTypeModelTest(TestCase):
    def test_str(self):
        dish_type = DishType.objects.create(name="Soup")
        self.assertEqual(str(dish_type), "Soup")


class CookModelTest(TestCase):
    def test_str(self):
        cook = get_user_model().objects.create_user(
            username="cook1",
            first_name="Gordon",
            last_name="Ramsay",
            years_of_experience=10,
            password="test1234"
        )

        self.assertEqual(str(cook), "cook1 (Gordon Ramsay)")

    def test_get_absolute_url(self):
        cook = get_user_model().objects.create_user(
            username="cook2",
            years_of_experience=5,
            password="test1234"
        )

        self.assertEqual(
            cook.get_absolute_url(),
            reverse("kitchen:cook-detail", kwargs={"pk": cook.pk})
        )


class DishModelTest(TestCase):
    def test_str(self):
        dish_type = DishType.objects.create(name="Dessert")
        cook = get_user_model().objects.create_user(
            username="cook3",
            years_of_experience=3,
            password="test1234"
        )

        dish = Dish.objects.create(
            name="Cheesecake",
            description="Classic cheesecake",
            price=10,
            dish_type=dish_type
        )
        dish.cooks.add(cook)

        self.assertEqual(str(dish), "Cheesecake")
