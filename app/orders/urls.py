
from django.urls import path

from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    DishesListView,
    DishesDetailView,
    DishesCreateView,
    DishesUpdateView,
    DishesDeleteView,
    revenue_report,
)


urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("order/new/", OrderCreateView.as_view(), name="order_create"),
    path("order/<int:pk>/edit/", OrderUpdateView.as_view(), name="order_update"),
    path("order/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("dishes/", DishesListView.as_view(), name="dishes_list"),
    path("dishes/<int:pk>/", DishesDetailView.as_view(), name="dishes_detail"),
    path("create/", DishesCreateView.as_view(), name="dishes_create"),
    path("dishes/<int:pk>/edit/", DishesUpdateView.as_view(), name="dishes_update"),
    path("dishes/<int:pk>/delete/", DishesDeleteView.as_view(), name="dishes_delete"),
    path("report/", revenue_report, name="report"),
]
