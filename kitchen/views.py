from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import get_object_or_404

from kitchen.models import Cook, Dish, DishType
from kitchen.forms import (
    CookCreationForm,
    CookExperienceUpdateForm,
    DishForm,
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
)


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "kitchen/index.html"

    def dispatch(self, request, *args, **kwargs):
        self.num_visits = request.session.get("num_visits", 0) + 1
        request.session["num_visits"] = self.num_visits
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cooks"] = Cook.objects.count()
        context["num_dishes"] = Dish.objects.count()
        context["num_dish_types"] = DishType.objects.count()
        context["num_visits"] = self.num_visits
        return context


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    paginate_by = 5

    def get_queryset(self):
        queryset = DishType.objects.all()
        self.search_form = DishTypeSearchForm(self.request.GET)

        if self.search_form.is_valid():
            return queryset.filter(
                name__icontains=self.search_form.cleaned_data["name"]
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        return context


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dishtype-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dishtype-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dishtype-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        self.search_form = DishSearchForm(self.request.GET)

        if self.search_form.is_valid():
            return queryset.filter(
                name__icontains=self.search_form.cleaned_data["name"]
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        return context


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish = self.object
        context["is_assigned"] = dish.cooks.filter(pk=self.request.user.pk).exists()
        return context


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_queryset(self):
        queryset = Cook.objects.all()
        self.search_form = CookSearchForm(self.request.GET)

        if self.search_form.is_valid():
            return queryset.filter(
                username__icontains=self.search_form.cleaned_data["username"]
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        return context


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class ToggleAssignToDishView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=kwargs["pk"])
        cook = request.user

        if dish.cooks.filter(pk=cook.pk).exists():
            dish.cooks.remove(cook)
        else:
            dish.cooks.add(cook)

        return HttpResponseRedirect(reverse("kitchen:dish-detail", args=[dish.pk]))

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
