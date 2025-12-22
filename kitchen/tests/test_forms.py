from django.test import TestCase
from django.contrib.auth import get_user_model

from kitchen.forms import DishSearchForm, DishForm
from kitchen.models import DishType


class DishSearchFormTest(TestCase):
    def test_search_form_valid(self):
        form = DishSearchForm(data={"name": "Borscht"})
        self.assertTrue(form.is_valid())

    def test_search_form_empty(self):
        form = DishSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())


class DishFormTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Soup")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345",
            years_of_experience=5,
        )

    def test_dish_form_valid(self):
        form_data = {
            "name": "Borscht",
            "description": "Traditional Ukrainian soup",
            "dish_type": self.dish_type.id,
            "price": 5,
            "cooks": [self.user.id],
        }

        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_form_invalid(self):
        form = DishForm(data={
            "name": "",
            "dish_type": "",
            "price": "",
        })
        self.assertFalse(form.is_valid())
