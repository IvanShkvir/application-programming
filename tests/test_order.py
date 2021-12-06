import requests
import pytest
from app import *

from tests.test_user import login_as_admin, login_as_user

url = 'http://127.0.0.1:5000'


def test_order_post():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.post(url + f'/orders', headers=headers, json={
        "id": 10,
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 3,
        "car_id": 2
    })
    assert res.status_code == 400
    res2 = requests.post(url + f'/orders', headers=headers, json={})
    assert res2.status_code == 400
    res3 = requests.post(url + f'/orders', headers=headers, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": True,
        "user_id": 4,
        "car_id": 6
    })
    assert res3.status_code == 400
    res4 = requests.post(url + f'/orders', headers=headers, json={
        "start_date": "2003-10-24",
        "end_date": "2003-10-23",
        "is_complete": False,
        "user_id": 3,
        "car_id": 7})
    assert res4.status_code == 400
    res5 = requests.post(url + f'/orders', headers=headers, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 1000,
        "car_id": 2})
    assert res5.status_code == 404
    res6 = requests.post(url + f'/orders', headers=headers, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 4,
        "car_id": 2})
    assert res6.status_code == 403
    res7 = requests.post(url + f'/orders', headers=headers, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 3,
        "car_id": 1000})
    assert res7.status_code == 404
    res8 = requests.post(url + f'/orders', headers=headers, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 3,
        "car_id": 10})
    assert res8.status_code == 400

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res9 = requests.post(url + f'/orders', headers=headers2, json={
        "id": 10,
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 3,
        "car_id": 2
    })
    assert res9.status_code == 400
    res10 = requests.post(url + f'/orders', headers=headers2, json={})
    assert res10.status_code == 400
    res11 = requests.post(url + f'/orders', headers=headers2, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": True,
        "user_id": 4,
        "car_id": 6
    })
    assert res11.status_code == 400
    res12 = requests.post(url + f'/orders', headers=headers2, json={
        "start_date": "2003-10-24",
        "end_date": "2003-10-23",
        "is_complete": False,
        "user_id": 4,
        "car_id": 7})
    assert res12.status_code == 400
    res13 = requests.post(url + f'/orders', headers=headers2, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 1000,
        "car_id": 2})
    assert res13.status_code == 404
    res14 = requests.post(url + f'/orders', headers=headers2, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 3,
        "car_id": 6})
    assert res14.status_code == 403
    res15 = requests.post(url + f'/orders', headers=headers2, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 4,
        "car_id": 1000})
    assert res15.status_code == 404
    res16 = requests.post(url + f'/orders', headers=headers2, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 4,
        "car_id": 10})
    assert res16.status_code == 400
    res17 = requests.post(url + f'/orders', headers=headers, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 3,
        "car_id": 8})
    assert res17.status_code == 200
    res18 = requests.post(url + f'/orders', headers=headers2, json={
        "start_date": "2003-10-23",
        "end_date": "2003-10-24",
        "is_complete": False,
        "user_id": 4,
        "car_id": 17})
    assert res18.status_code == 200


def test_order_get():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.get(url + f'/order/2', headers=headers)
    assert res.status_code == 200
    res2 = requests.get(url + f'/order/1000', headers=headers)
    assert res2.status_code == 404
    res3 = requests.get(url + f'/order/1', headers=headers)
    assert res3.status_code == 403

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res4 = requests.get(url + f'/order/1', headers=headers2)
    assert res4.status_code == 200
    res5 = requests.get(url + f'/order/1000', headers=headers2)
    assert res5.status_code == 404
    res6 = requests.get(url + f'/order/2', headers=headers2)
    assert res6.status_code == 403


def test_delete_order():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.delete(url + f'/order/1000', headers=headers)
    assert res.status_code == 404
    res2 = requests.delete(url + f'/order/1', headers=headers)
    assert res2.status_code == 403
    order_id = s.query(Order).all()[-1].id
    res3 = requests.delete(url + f'/order/{order_id}', headers=headers)
    assert res3.status_code == 403

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res4 = requests.delete(url + f'/order/1000', headers=headers2)
    assert res4.status_code == 404
    res5 = requests.delete(url + f'/order/2', headers=headers2)
    assert res5.status_code == 403


def test_order_update():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + f'/order/2', headers=headers, json={
        "id": 100
    })
    assert res.status_code == 400
    res2 = requests.put(url + f'/order/2', headers=headers, json={})
    assert res2.status_code == 400
    res3 = requests.put(url + f'/order/2', headers=headers, json={
        "user_id": 1000
    })
    assert res3.status_code == 404
    res4 = requests.put(url + f'/order/1', headers=headers, json={
        "end_date": "2020-11-12"
    })
    assert res4.status_code == 403
    res5 = requests.put(url + f'/order/2', headers=headers, json={
        "car_id": 1000
    })
    assert res5.status_code == 404
    res6 = requests.put(url + f'/order/2', headers=headers, json={
        "car_id": 3
    })
    assert res6.status_code == 400
    res7 = requests.put(url + f'/order/2', headers=headers, json={
        "start_date": "2020-10-10",
        "end_date": "2020-11-21"
    })
    assert res7.status_code == 200



    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res8 = requests.put(url + f'/order/1', headers=headers2, json={
        "id": 100
    })
    assert res8.status_code == 400
    res9 = requests.put(url + f'/order/1', headers=headers2, json={})
    assert res9.status_code == 400
    res10 = requests.put(url + f'/order/1', headers=headers2, json={
        "user_id": 1000
    })
    assert res10.status_code == 404
    res11 = requests.put(url + f'/order/2', headers=headers2, json={
        "end_date": "2020-11-12"
    })
    assert res11.status_code == 403
    res12 = requests.put(url + f'/order/1', headers=headers2, json={
        "car_id": 1000
    })
    assert res12.status_code == 404
    res13 = requests.put(url + f'/order/1', headers=headers2, json={
        "car_id": 3
    })
    assert res13.status_code == 400
    res14 = requests.put(url + f'/order/1', headers=headers2, json={
        "start_date": "2020-10-10",
        "end_date": "2020-11-22"
    })
    assert res14.status_code == 200
