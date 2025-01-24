from decimal import ROUND_HALF_UP, Decimal
from typing import List
from pydantic import BaseModel,field_validator
from pytest import fixture
from orders.models import Dishes, Orders


class DishInput(BaseModel):
    dish: str
    descr: str
    price: Decimal

    @field_validator("price")
    def format_price(cls, v):
        return Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class OrderInput(BaseModel):
    table_number: int
    status: str
    items_ids: List[int]

@fixture(scope="function")
def first_dish_data():
    dish = DishInput(dish="Паста", descr="Вкусная паста", price=20.00)
    return dish

@fixture(scope="function")
def second_dish_data():
    dish = DishInput(dish="Пицца", descr="Вкусная паста", price=15.00)
    return dish


dish1_input_data = DishInput(dish="Паста", descr="Вкусная паста", price=20.00) 
dish2_input_data = DishInput(dish="Пицца", descr="Вкусная паста", price=15.00)
order_input_data = OrderInput(table_number=2, status="Ожидает", items_ids=[])


@fixture(scope="function", autouse=True)
def django_db_setup():
    pass


@fixture
def add_dishes(scope="function"):

    dish1 = Dishes.objects.create(
        dish=dish1_input_data.dish,
        descr=dish1_input_data.descr,
        price=dish1_input_data.price,
    )
    dish2 = Dishes.objects.create(
        dish=dish2_input_data.dish,
        descr=dish2_input_data.descr,
        price=dish2_input_data.price,
    )
    return [dish1.id, dish2.id]


@fixture
def clear_db(scope="function"):

    yield

    for order in Orders.objects.all():
        order.items.clear()
    Orders.objects.all().delete()
    Dishes.objects.all().delete()
