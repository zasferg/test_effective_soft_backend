import pytest
from tests.testlib.api_requests import (
    get_dishes_api_request,
    get_dish_by_id_api_request,
    create_dish_api_request,
    update_dish_api_request,
)


import pytest


@pytest.mark.django_db(transaction=True)
def test_create_and_get_dish(clear_db, first_dish_data, second_dish_data):
    """
    Тест для создания и получения всех блюд.
    """
    dish1_data = first_dish_data
    dish2_data = second_dish_data
    # Создание первых двух блюд через API
    create_dish_api_request(data=dish1_data.model_dump())
    create_dish_api_request(data=dish2_data.model_dump())

    # Получение всех блюд через API
    get_all_dishes_response = get_dishes_api_request()
    # Проверка, что запрос успешен
    assert get_all_dishes_response.status_code == 200

    get_all_dishes_response_json = get_all_dishes_response.json()

    # Получение первого и второго блюда из ответа
    first_dish = get_all_dishes_response_json[0]
    second_dish = get_all_dishes_response_json[1]

    # Проверка, что в ответе два блюда
    assert len(get_all_dishes_response_json) == 2

    # Проверка, что данные первого и второго блюда совпадают с исходными
    assert first_dish["dish"] == dish1_data.dish
    assert second_dish["dish"] == dish2_data.dish


@pytest.mark.django_db(transaction=True)
def test_get_by_id_and_update_dish(clear_db, first_dish_data):
    """
    Тест для получения блюда по ID и его обновления.
    """

    dish1_data = first_dish_data

    # Создание блюда через API
    dish_response = create_dish_api_request(data=dish1_data.model_dump())

    # Получение ID созданного блюда
    dish_id = dish_response.json()["id"]

    # Получение блюда по ID через API
    get_dish_by_id_response = get_dish_by_id_api_request(id=dish_id)

    # Проверка, что запрос успешен
    assert get_dish_by_id_response.status_code == 200

    get_dish_by_id_response_json = get_dish_by_id_response.json()

    # Проверка, что данные блюда совпадают с исходными
    assert get_dish_by_id_response_json["dish"] == dish1_data.dish
    assert get_dish_by_id_response_json["descr"] == dish1_data.descr
    assert get_dish_by_id_response_json["price"] == str(dish1_data.price)

    # Обновление данных блюда
    dish1_data.dish = "Рыба"
    dish1_data.descr = "Вкусная рыба"

    # Обновление блюда через API
    update_dish_api_request(id=dish_id, data=dish1_data.model_dump())

    # Получение обновленного блюда по ID через API
    get_updated_dish_response = get_dish_by_id_api_request(id=dish_id)

    # Проверка, что запрос успешен
    assert get_updated_dish_response.status_code == 200

    get_updated_dish_response_json = get_updated_dish_response.json()

    # Проверка, что данные обновленного блюда совпадают с новыми данными
    assert get_updated_dish_response_json["dish"] == dish1_data.dish
    assert get_updated_dish_response_json["descr"] == dish1_data.descr
    assert get_updated_dish_response_json["price"] == str(dish1_data.price)
