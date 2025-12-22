from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import Dish, DishType


class DishListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

        self.dish_type = DishType.objects.create(name="Soup")
        self.dish = Dish.objects.create(
            name="Borscht",
            dish_type=self.dish_type,
            price=5,
        )

    def test_dish_list_view_status_code(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)

    def test_dish_list_view_uses_correct_template(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_dish_list_contains_dish(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertContains(response, "Borscht")

    def test_dish_search(self):
        response = self.client.get(
            reverse("kitchen:dish-list"),
            {"name": "Borscht"},
        )
        self.assertContains(response, "Borscht")


class DishDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

        self.dish_type = DishType.objects.create(name="Main")
        self.dish = Dish.objects.create(
            name="Steak",
            dish_type=self.dish_type,
            price=10,
        )

    def test_dish_detail_view(self):
        response = self.client.get(
            reverse("kitchen:dish-detail", args=[self.dish.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Steak")
