import requests
import pytest
from app import *

from tests.test_user import login_as_admin, login_as_user

url = 'http://127.0.0.1:5000'


def test_car_post():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.post(url + f'/cars', headers=headers, json={
        "model": "model",
        "brand": "brand",
        "status": "available",
        "price": 1000})
    assert res.status_code == 200
    res2 = requests.post(url + f'/cars', headers=headers, json={
        "id": 5,
        "model": "model",
        "brand": "brand",
        "status": "available",
        "price": 1000})
    assert res2.status_code == 400
    res3 = requests.post(url + f'/cars', headers=headers, json={})
    assert res3.status_code == 400
    res4 = requests.post(url + f'/cars', headers=headers, json={
        "model": "model",
        "brand": "brand",
        "status": "reserved",
        "price": 1000})
    assert res4.status_code == 400
    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res5 = requests.post(url + f'/cars', headers=headers2, json={
        "model": "model",
        "brand": "brand",
        "status": "available",
        "price": 1000})
    assert res5.status_code == 403


def test_cars_get():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.get(url + f'/cars', headers=headers)
    assert res.status_code == 200

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res2 = requests.get(url + f'/cars', headers=headers2)
    assert res2.status_code == 200


def test_car_get():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.get(url + f'/car/1', headers=headers)
    assert res.status_code == 200 and res.json()["model"] == "surname123"

    res2 = requests.get(url + f'/car/1000', headers=headers)
    assert res2.status_code == 404

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res3 = requests.get(url + f'/car/1', headers=headers2)
    assert res3.status_code == 200

    res4 = requests.get(url + f'/car/1000', headers=headers2)
    assert res4.status_code == 404


def test_update_car():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + f'/car/1', headers=headers, json={
        "id": 6
    })
    assert res.status_code == 400
    res2 = requests.put(url + f'/car/1', headers=headers, json={
        "status": "reserved"
    })
    assert res2.status_code == 400
    res3 = requests.put(url + f'/car/1', headers=headers, json={})
    assert res3.status_code == 400
    res4 = requests.put(url + f'/car/1000', headers=headers, json={
        "model": "someName"
    })
    assert res4.status_code == 404

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res5 = requests.put(url + f'/car/1', headers=headers2, json={
        "model": "someName"
    })
    assert res5.status_code == 403

    res6 = requests.put(url + f'/car/1', headers=headers, json={
        "model": "surname123"
    })
    assert res6.status_code == 200


def test_delete_car():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.delete(url + f'/car/1000', headers=headers)
    assert res.status_code == 404
    res2 = requests.delete(url + f'/car/1', headers=headers)
    assert res2.status_code == 400

    car_id = s.query(Car).filter(Car.model == "model").all()[-1].id
    res3 = requests.delete(url + f'/car/{car_id}', headers=headers)
    assert res3.status_code == 200

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res4 = requests.delete(url + f'/car/1', headers=headers2)
    assert res4.status_code == 403
