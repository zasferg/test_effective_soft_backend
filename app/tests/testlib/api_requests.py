from decimal import Decimal
import json
import requests


host = "http://127.0.0.1:8000/api"


def create_order_api_request(data):
    response = requests.post(url=f"{host}/orders/", json=data)
    return response


def get_orders_api_request():
    response = requests.get(url=f"{host}/orders/")
    return response


def get_order_by_id_api_request(id):
    response = requests.get(url=f"{host}/orders/{id}/")
    return response


def update_order_api_request(id, data):
    response = requests.put(url=f"{host}/orders/{id}/", json=data)
    return response


def get_report_api_request():
    response = requests.get(url=f"{host}/report")
    return response


def create_dish_api_request(data):
    for key, value in data.items():
        if isinstance(value, Decimal):
            data[key] = float(value)
    response = requests.post(url=f"{host}/dishes/", json=data)
    return response


def get_dishes_api_request():
    response = requests.get(url=f"{host}/dishes/")
    return response


def get_dish_by_id_api_request(id):
    response = requests.get(url=f"{host}/dishes/{id}/")
    return response


def update_dish_api_request(id, data):
    for key, value in data.items():
        if isinstance(value, Decimal):
            data[key] = float(value)
    response = requests.put(url=f"{host}/dishes/{id}/", json=data)
    return response
