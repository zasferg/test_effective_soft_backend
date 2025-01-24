from django import forms
from orders.models import Orders, Dishes


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказов.
    """

    class Meta:
        model = Orders
        fields = ["table_number", "items", "status"]
        labels = {
            "table_number": "Номер столика",
            "items": "Блюда",
            "status": "Статус заказа",
        }

        widgets = {
            "status": forms.Select(choices=Orders.Status.choices),
            "items": forms.CheckboxSelectMultiple,
        }


class DishesForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ["dish", "descr", "price"]
        labels = {
            "dish": "Блюдо",
            "descr": "Описание",
            "price": "Цена",
        }
