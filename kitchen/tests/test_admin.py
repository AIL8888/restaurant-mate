from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType
from kitchen.admin import DishAdmin


class AdminSiteTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            years_of_experience=5
        )
        self.client.force_login(self.admin_user)

    def test_admin_page_accessible(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)


class AdminModelRegistrationTest(TestCase):
    def test_dish_registered_in_admin(self):
        self.assertIn(Dish, admin.site._registry)

    def test_dishtype_registered_in_admin(self):
        self.assertIn(DishType, admin.site._registry)


class DishAdminTest(TestCase):
    def test_dish_admin_list_display(self):
        self.assertEqual(
            DishAdmin.list_display,
            ("name", "dish_type", "price")
        )

    def test_dish_admin_search_fields(self):
        self.assertEqual(
            DishAdmin.search_fields,
            ("name",)
        )

    def test_dish_admin_list_filter(self):
        self.assertEqual(
            DishAdmin.list_filter,
            ("dish_type",)
        )


class AdminDishPageTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            years_of_experience=5
        )
        self.client.force_login(self.admin_user)

        self.dish_type = DishType.objects.create(name="Soup")
        self.dish = Dish.objects.create(
            name="Borscht",
            dish_type=self.dish_type,
            price=5.00
        )

    def test_dish_change_page(self):
        url = reverse("admin:kitchen_dish_change", args=[self.dish.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Borscht")
