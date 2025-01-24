from decimal import Decimal
import pytest
import random
from tests.conftest import order_input_data
from tests.testlib.api_requests import (
    get_orders_api_request,
    get_order_by_id_api_request,
    update_order_api_request,
    create_order_api_request,
    get_report_api_request,
)


@pytest.mark.django_db(transaction=True)
def test_create_and_get_order(clear_db, add_dishes, first_dish_data, second_dish_data):
    """
    Тест для добавления заказа и получения списка заказов.
    """
    order_dish1_data = first_dish_data
    order_dish2_data = second_dish_data
    # Устанавливаем идентификаторы блюд для заказа
    order_input_data.items_ids = add_dishes

    # Создаем заказ с указанными данными
    create_order_response = create_order_api_request(data=order_input_data.model_dump())
    assert create_order_response.status_code == 201

    # Получаем ID созданного заказа
    order_id = create_order_response.json()["id"]

    # Получаем все заказы
    all_orders_response = get_orders_api_request()
    all_orders_response_json = all_orders_response.json()
    print(all_orders_response_json)
    # Проверяем, что запрос успешен и создан только один заказ
    assert all_orders_response.status_code == 200
    assert len(all_orders_response_json) == 1
    assert all_orders_response_json[0]["id"] == order_id

    # Получаем заказ по ID
    order_response = get_order_by_id_api_request(id=order_id)
    order_response_json = order_response.json()
    order_dishes_data = order_response_json["items"]
    first_dish = order_dishes_data[0]
    second_dish = order_dishes_data[1]

    # Проверяем данные заказа
    assert order_response.status_code == 200
    assert order_response_json["table_number"] == order_input_data.table_number
    assert order_response_json["status"] == order_input_data.status
    assert len(order_dishes_data) == 2
    assert first_dish["dish"] == order_dish1_data.dish
    assert first_dish["descr"] == order_dish1_data.descr
    assert first_dish["price"] == str(order_dish1_data.price)
    assert second_dish["dish"] == order_dish2_data.dish
    assert second_dish["descr"] == order_dish2_data.descr
    assert second_dish["price"] == str(order_dish2_data.price)
    assert order_response_json["total_price"] == str(
        order_dish1_data.price + order_dish2_data.price
    )

    # Проверяем, что запрос с неправильным ID возвращает 404
    wrong_id = order_id + random.randint(1, 100)
    wrong_id_order_response = get_order_by_id_api_request(id=wrong_id)
    assert wrong_id_order_response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_update_order_and_get_report(clear_db, add_dishes):
    """
    Тест для получения заказа по ID , его обновления и произведения расчетов за смену.
    """
    order_data = order_input_data
    # Устанавливаем идентификаторы блюд для заказа
    order_data.items_ids = add_dishes

    # Создаем заказ с указанными данными
    create_order_response = create_order_api_request(data=order_input_data.model_dump())
    assert create_order_response.status_code == 201

    # Обновляем статус и номер стола заказа
    update_status_data = "Готов"
    update_table_number_data = 3
    order_id = create_order_response.json()["id"]
    order_input_data.status = update_status_data
    order_input_data.table_number = update_table_number_data

    # Отправляем запрос на обновление заказа
    update_order_api_request(id=order_id, data=order_input_data.model_dump())
    # Получаем заказ по ID
    updated_order_response = get_order_by_id_api_request(id=order_id)
    updated_order_data = updated_order_response.json()

    # Проверяем данные обновленного заказа
    assert updated_order_response.status_code == 200
    assert updated_order_data["status"] == update_status_data
    assert updated_order_data["table_number"] == update_table_number_data

    # Пытаемся обновить заказ с неправильным статусом
    update_status_data = "bad_value"
    order_input_data.status = update_status_data
    wrong_status_updated_order_response = update_order_api_request(
        id=order_id, data=order_input_data.model_dump()
    )
    assert wrong_status_updated_order_response.status_code == 400

    # Получаем все заказы и рассчитываем общую сумму
    get_all_orders = get_orders_api_request().json()
    total = sum(Decimal(order["total_price"]) for order in get_all_orders)

    # Получаем отчет и проверяем его корректность
    get_report = get_report_api_request()
    expected_message = f"Выручка за день составила {total} руб."
    message_from_url = get_report.json()["message"]
    assert expected_message == message_from_url
