from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.models import Cook, Dish, DishType


class PublicPagesTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivatePagesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
            years_of_experience=3,
        )
        self.client.force_login(self.user)


class SearchTests(PrivatePagesTests):
    def setUp(self):
        super().setUp()

        self.cook1 = Cook.objects.create_user(
            username="john",
            password="pass",
            years_of_experience=5,
        )
        self.cook2 = Cook.objects.create_user(
            username="mike",
            password="pass",
            years_of_experience=2,
        )

        self.dish_type1 = DishType.objects.create(name="Soup")
        self.dish_type2 = DishType.objects.create(name="Main")

        self.dish1 = Dish.objects.create(
            name="Borscht",
            dish_type=self.dish_type1,
            price=5,
        )
        self.dish2 = Dish.objects.create(
            name="Steak",
            dish_type=self.dish_type2,
            price=10,
        )

    def test_cook_search(self):
        response = self.client.get(
            reverse("kitchen:cook-list"),
            {"username": "john"},
        )
        self.assertContains(response, "john")
        self.assertNotContains(response, "mike")

    def test_dish_search(self):
        response = self.client.get(
            reverse("kitchen:dish-list"),
            {"name": "Borscht"},
        )
        self.assertContains(response, "Borscht")
        self.assertNotContains(response, "Steak")

    def test_dish_type_search(self):
        response = self.client.get(
            reverse("kitchen:dishtype-list"),
            {"name": "Soup"},
        )
        self.assertContains(response, "Soup")
        self.assertNotContains(response, "Main")
