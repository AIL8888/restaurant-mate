from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish, Cook


class KitchenURLsTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create_user(
            username="cook1", password="pass", years_of_experience=3
        )
        self.client.force_login(self.cook)
        self.dishtype = DishType.objects.create(name="Soup")
        self.dish = Dish.objects.create(
            name="Borscht",
            description="Traditional Ukrainian soup",
            price=5,
            dish_type=self.dishtype
        )
        self.dish.cooks.add(self.cook)

    def test_index_url(self):
        response = self.client.get(reverse("kitchen:index"))
        self.assertEqual(response.status_code, 200)

    def test_dishtype_list_url(self):
        response = self.client.get(reverse("kitchen:dishtype-list"))
        self.assertEqual(response.status_code, 200)

    def test_dishtype_create_url(self):
        response = self.client.get(reverse("kitchen:dishtype-create"))
        self.assertEqual(response.status_code, 200)

    def test_dishtype_update_url(self):
        response = self.client.get(
            reverse("kitchen:dishtype-update", args=[self.dishtype.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_dishtype_delete_url(self):
        response = self.client.get(
            reverse("kitchen:dishtype-delete", args=[self.dishtype.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_dish_list_url(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)

    def test_dish_detail_url(self):
        response = self.client.get(
            reverse("kitchen:dish-detail", args=[self.dish.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_dish_create_url(self):
        response = self.client.get(reverse("kitchen:dish-create"))
        self.assertEqual(response.status_code, 200)

    def test_dish_update_url(self):
        response = self.client.get(
            reverse("kitchen:dish-update", args=[self.dish.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_dish_delete_url(self):
        response = self.client.get(
            reverse("kitchen:dish-delete", args=[self.dish.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_dish_toggle_assign_url(self):
        response = self.client.get(
            reverse("kitchen:toggle-dish-assign", args=[self.dish.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_cook_list_url(self):
        response = self.client.get(reverse("kitchen:cook-list"))
        self.assertEqual(response.status_code, 200)

    def test_cook_detail_url(self):
        response = self.client.get(
            reverse("kitchen:cook-detail", args=[self.cook.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_cook_create_url(self):
        response = self.client.get(reverse("kitchen:cook-create"))
        self.assertEqual(response.status_code, 200)

    def test_cook_update_url(self):
        response = self.client.get(
            reverse("kitchen:cook-update", args=[self.cook.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_cook_delete_url(self):
        response = self.client.get(
            reverse("kitchen:cook-delete", args=[self.cook.id])
        )
        self.assertEqual(response.status_code, 200)
