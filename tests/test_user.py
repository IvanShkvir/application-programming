from app import *
import requests
import pytest

url = 'http://127.0.0.1:5000'


def login_as_admin():
    headers = {'Authorization': "Basic c3BlY2lhbDpxd2VydHk="}
    res = requests.post(url + '/auth/login', headers=headers)
    access_token = res.json()["token"]
    return access_token


def login_as_user():
    headers = {'Authorization': "Basic b3JkaW5hcnk6cXdlcnR5MQ=="}
    res = requests.post(url + '/auth/login', headers=headers)
    access_token = res.json()["token"]
    return access_token


def test_user_get():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.get(url + f'/user/3', headers=headers)
    assert res.status_code == 200
    res2 = requests.get(url + f'/user/1000', headers=headers)
    assert res2.status_code == 404
    res3 = requests.get(url + f'/user/4', headers=headers)
    assert res3.status_code == 403

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res = requests.get(url + f'/user/4', headers=headers2)
    assert res.status_code == 200
    res2 = requests.get(url + f'/user/1000', headers=headers2)
    assert res2.status_code == 404
    res3 = requests.get(url + f'/user/3', headers=headers2)
    assert res3.status_code == 403


def test_user_update():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + f'/user/3', headers=headers, json={})
    assert res.status_code == 400
    res2 = requests.put(url + f'/user/3', headers=headers, json={
        "id": 6
    })
    assert res2.status_code == 400
    res3 = requests.put(url + f'/user/1000', headers=headers, json={
        "name": "someUser"
    })
    assert res3.status_code == 400
    res4 = requests.put(url + f'/user/4', headers=headers, json={
        "name": "someName"
    })
    assert res4.status_code == 403
    res5 = requests.put(url + f'/user/3', headers=headers, json={
        "username": "ordinary"
    })
    assert res5.status_code == 400
    res6 = requests.put(url + f'/user/3', headers=headers, json={
        "name": "someName"
    })
    assert res6.status_code == 200

    headers2 = {'Authorization': 'Bearer ' + login_as_user()}
    res7 = requests.put(url + f'/user/4', headers=headers2, json={})
    assert res7.status_code == 400
    res8 = requests.put(url + f'/user/4', headers=headers2, json={
        "id": 6
    })
    assert res8.status_code == 400
    res9 = requests.put(url + f'/user/1000', headers=headers2, json={
        "name": "someUser"
    })
    assert res9.status_code == 400
    res10 = requests.put(url + f'/user/3', headers=headers2, json={
        "name": "someName"
    })
    assert res10.status_code == 403
    res11 = requests.put(url + f'/user/4', headers=headers2, json={
        "username": "ordinary"
    })
    assert res11.status_code == 400
    res12 = requests.put(url + f'/user/4', headers=headers2, json={
        "name": "someName"
    })
    assert res12.status_code == 200
