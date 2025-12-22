from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from kitchen.models import Dish, Cook, DishType


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class CookExperienceMixin:
    def clean_years_of_experience(self):
        experience = self.cleaned_data.get("years_of_experience")
        if experience is not None and experience < 0:
            raise ValidationError("Experience cannot be negative")
        return experience


class CookCreationForm(UserCreationForm, CookExperienceMixin):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name"
        )


class CookExperienceUpdateForm(forms.ModelForm, CookExperienceMixin):
    class Meta:
        model = Cook
        fields = ["years_of_experience"]


class CookSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by dish name"})
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by category name"}
        )
    )
