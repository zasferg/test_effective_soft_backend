from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Orders, Dishes
from .forms import OrderForm, DishesForm
from datetime import datetime
from django.db.models import Sum
from django.http import HttpRequest
from typing import Any, Dict


class OrderListView(ListView):
    """
    Представление для отображения списка заказов.
    """

    model = Orders
    template_name = "order_list.html"
    context_object_name = "orders"


class OrderDetailView(DetailView):
    """
    Представление для отображения деталей конкретного заказа.
    """

    model = Orders
    template_name = "order_detail.html"
    context_object_name = "order"


class OrderCreateView(CreateView):
    """
    Представление для создания нового заказа.
    """

    model = Orders
    form_class = OrderForm
    template_name = "order_form.html"
    success_url = reverse_lazy("order_list")

    def form_valid(self, form: OrderForm) -> HttpResponse:
        """
        Обрабатывает валидную форму и сохраняет новый заказ.
        """
        if form.is_valid():
            new_order = Orders(
                table_number=form.data["table_number"], status=form.data["status"]
            )
            new_order.save()
            new_order.items.add(*form.cleaned_data["items"])
            new_order.save()
            return HttpResponse(f"Заказ добавлен")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать новый заказ"
        return context


class OrderUpdateView(UpdateView):
    """
    Представление для обновления существующего заказа.
    """

    model = Orders
    form_class = OrderForm
    template_name = "order_form.html"
    success_url = reverse_lazy("order_list")

    def form_valid(self, form: OrderForm) -> HttpResponse:
        """
        Обрабатывает валидную форму и сохраняет обновленный заказ.
        """
        order = form.save(commit=False)
        order.calculate_total_price()
        order.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Обновить заказ"
        return context


class OrderDeleteView(DeleteView):
    """
    Представление для удаления заказа.
    """

    model = Orders
    template_name = "order_delete.html"
    success_url = reverse_lazy("order_list")


class DishesListView(ListView):
    """
    Представление для отображения списка блюд.
    """

    model = Dishes
    template_name = "dishes_list.html"
    context_object_name = "dishes"


class DishesDetailView(DetailView):
    """
    Представление для отображения деталей конкретного блюда.
    """

    model = Dishes
    template_name = "dishes_detail.html"
    context_object_name = "dish"


class DishesCreateView(CreateView):
    model = Dishes
    form_class = DishesForm
    template_name = "dishes_form.html"
    success_url = reverse_lazy("dishes_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать блюдо"
        return context


class DishesUpdateView(UpdateView):
    model = Dishes
    form_class = DishesForm
    template_name = "dishes_form.html"
    success_url = reverse_lazy("dishes_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Обновить блюдо"
        return context


class DishesDeleteView(DeleteView):
    model = Dishes
    template_name = "dishes_delete.html"
    success_url = reverse_lazy("dishes_list")


def revenue_report(request: HttpRequest) -> HttpResponse:
    """
    Представление для отображения отчета о выручке за текущий день.
    """
    today = datetime.now()
    start_of_shift = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_shift = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    report = (
        Orders.objects.filter(
            status=Orders.Status.READY, created_at__range=(start_of_shift, end_of_shift)
        ).aggregate(total_revenue=Sum("total_price"))["total_revenue"]
        or 0
    )
    return render(request, "report.html", {"report": report})
