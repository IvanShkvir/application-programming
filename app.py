import datetime

from flask import jsonify, request
from schemes import *
from models import *
from marshmallow import ValidationError
from flask import Blueprint
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker

from utils import get_value_from_json

api_blueprint = Blueprint('api_blueprint', __name__)

session = sessionmaker(bind=engine)
s = session()


@api_blueprint.route('/auth/register', methods=['POST'])
def create_user():
    json_user_data = request.get_json()

    if 'id' in json_user_data:
        return {"message": "You can not set id"}, 400
    if 'role' not in json_user_data:
        return {"message": "You should specify a role"}, 400
    if not json_user_data:
        return {"message": "Empty request body"}, 400

    if json_user_data['password']:
        json_user_data['password'] = Bcrypt().generate_password_hash(json_user_data['password']).decode('utf - 8')
    try:
        user_data = UserSchema().load(json_user_data)
    except ValidationError as err:
        return err.messages, 400

    if s.query(User).filter_by(username=json_user_data['username']).first():
        return {"message": "User with provided username already exists"}, 400

    user = User(**user_data)
    s.add(user)
    s.commit()
    serialized_user = UserSchema().dump(user)
    return jsonify(serialized_user)


@api_blueprint.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = s.query(User).filter_by(id=id).first()
    if not user:
        return {"message": "User with provided id does not exist"}, 404
    serialized_user = UserSchema().dump(user)
    return jsonify(serialized_user)


@api_blueprint.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    json_user_data = request.get_json()
    if not json_user_data:
        return {"message": "Empty request body"}, 400
    if 'id' in json_user_data:
        return {"message": "You can not change id"}, 400

    user_check_id = s.query(User).filter_by(id=id).first()
    if not user_check_id:
        return {"message": "User with provided id does not exists"}, 400

    if 'username' in json_user_data:
        user_check_username = s.query(User).filter_by(name=json_user_data['name']).first()
        if user_check_username:
            return {"message": "User with provided username already exists"}, 400

    try:
        UserSchema().load(json_user_data)
    except ValidationError as err:
        return err.messages, 400

    for key, value in json_user_data.items():
        if key == 'password':
            value = Bcrypt().generate_password_hash(value).decode('utf - 8')

        setattr(user_check_id, key, value)
    s.commit()
    user_find = s.query(User).filter_by(id=id).first()
    serialized_user = UserSchema().dump(user_find)
    return jsonify(serialized_user)


@api_blueprint.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user_check_id = s.query(User).filter_by(id=id).first()
    if not user_check_id:
        return {"message": "User with provided id does not exists"}, 400

    if s.query(Order).filter_by(user_id=id).filter_by(is_complete=False).all():
        return {"message": "User has non-completed orders"}, 400

    serialized_user = UserSchema().dump(user_check_id)

    s.delete(user_check_id)
    s.commit()

    return jsonify(serialized_user)


@api_blueprint.route('/cars', methods=['GET'])
def get_cars():
    cars_find = s.query(Car).all()

    serialized_cars = []
    for car in cars_find:
        serialized_cars.append(car)
    return jsonify(serialized_cars)


@api_blueprint.route('/cars', methods=['POST'])
def create_car():
    json_car_data = request.get_json()

    if 'id' in json_car_data:
        return {"message": "You can not set id"}, 400
    if not json_car_data:
        return {"message": "Empty request body"}, 400
    if 'status' in json_car_data:
        if get_value_from_json(json_car_data, 'status') == "reserved":
            return {"message": "You cannot create already reserved car"}, 400
    try:
        car_data = CarSchema().load(json_car_data)
    except ValidationError as err:
        return err.messages, 400

    car = Car(**car_data)
    s.add(car)
    s.commit()
    serialized_car = CarSchema().dump(car)
    return jsonify(serialized_car)


@api_blueprint.route('/car/<int:id>', methods=['GET'])
def get_car(id):
    car = s.query(Car).filter_by(id=id).first()
    if not car:
        return {"message": "Car with provided id does not exist"}, 404
    serialized_car = CarSchema().dump(car)
    return jsonify(serialized_car)


@api_blueprint.route('/car/<int:id>', methods=['PUT'])
def update_car(id):
    json_car_data = request.get_json()
    if 'id' in json_car_data:
        return {"message": "You can not change id"}, 400
    if 'status' in json_car_data:
        return {"message": "You can not change status of car without order"}, 400
    if not json_car_data:
        return {"message": "Empty request body"}, 400

    car = s.query(Car).filter_by(id=id).first()
    if not car:
        return {"message": "Car with provided id does not exist"}, 404

    try:
        CarSchema().load(json_car_data)
    except ValidationError as err:
        return err.messages, 400
    for key, value in json_car_data.items():
        setattr(car, key, value)
    s.commit()
    car_find = s.query(Car).filter_by(id=id).first()
    serialized_car = CarSchema().dump(car_find)
    return jsonify(serialized_car)


@api_blueprint.route('/car/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = s.query(Car).filter_by(id=id).first()
    if not car:
        return {"message": "Car with provided id does not exist"}, 404
    if s.query(Order).filter_by(car_id=id).filter_by(is_complete=False).all():
        return {"message": "Car is related to order"}, 400

    serialized_car = CarSchema().dump(car)
    s.delete(car)
    s.commit()
    return jsonify(serialized_car)


@api_blueprint.route('/orders', methods=['POST'])
def create_order():
    json_order_data = request.get_json()

    if 'id' in json_order_data:
        return {"message": "You can not set id"}, 400
    if not json_order_data:
        return {"message": "Empty request body"}, 400

    if get_value_from_json(json_order_data, "is_complete"):
        return {"message": "Cannot create already completed order"}, 400

    if datetime.datetime.strptime(get_value_from_json(json_order_data, "end_date"), "%Y-%m-%d") < datetime.datetime.strptime(get_value_from_json(json_order_data, "start_date"), "%Y-%m-%d"):
        return {"message": "Invalid date range"}, 400

    try:
        order_data = OrderSchema().load(json_order_data)
    except ValidationError as err:
        return err.messages, 400

    user_find = s.query(User).filter_by(id=json_order_data['user_id']).first()
    car_find = s.query(Car).filter_by(id=json_order_data['car_id']).first()
    if not user_find:
        return {"message": "User with provided id does not exist"}, 404

    if not car_find:
        return {"message": "Car with provided id does not exist"}, 404

    if car_find.status == "reserved":
        return {"message": "Car is already reserved"}, 400

    setattr(car_find, "status", "reserved")

    order = Order(**order_data)
    s.add(order)
    s.commit()
    serialized_order = OrderSchema().dump(order)
    return jsonify(serialized_order)


@api_blueprint.route('/order/<int:id>', methods=['GET'])
def get_order(id):
    order = s.query(Order).filter_by(id=id).first()
    if not order:
        return {"message": "Order with provided id does not exist"}, 404
    serialized_order = CarSchema().dump(order)
    return jsonify(serialized_order)


@api_blueprint.route('/order/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = s.query(Order).filter_by(id=id).first()
    if not order:
        return {"message": "Order with provided id does not exist"}, 404
    car_find = s.query(Car).filter_by(id=order.car_id).first()
    setattr(car_find, "status", "available")
    serialized_order = CarSchema().dump(order)
    s.delete(order)
    s.commit()
    return jsonify(serialized_order)


@api_blueprint.route('/order/<int:id>', methods=['PUT'])
def update_order(id):
    json_order_data = request.get_json()
    if 'id' in json_order_data:
        return {"message": "You can not change id"}, 400
    if not json_order_data:
        return {"message": "Empty request body"}, 400
    try:
        OrderSchema().load(json_order_data)
    except ValidationError as err:
        return err.messages, 400
    order = s.query(Order).filter_by(id=id).first()
    if 'user_id' in json_order_data:
        user_find = s.query(User).filter_by(id=json_order_data['user_id']).first()
        if not user_find:
            return {"message": "User with provided id does not exist"}, 404
    if 'car_id' in json_order_data:
        car_find = s.query(Car).filter_by(id=json_order_data['car_id']).first()
        if not car_find:
            return {"message": "Car with provided id does not exist"}, 404
        if car_find.status == "reserved":
            return {"message": "Car is already reserved"}, 400
        if 'is_complete' in json_order_data:
            if get_value_from_json(json_order_data, 'is_complete'):
                setattr(car_find, "status", "available")
    if 'end_time' in json_order_data and 'start_time' in json_order_data:
        if datetime.datetime.strptime(get_value_from_json(json_order_data, "end_date"),
                                      "%Y-%m-%d") < datetime.datetime.strptime(
                get_value_from_json(json_order_data, "start_date"), "%Y-%m-%d"):
            return {"message": "Invalid date range"}, 400

    for key, value in json_order_data.items():
        setattr(order, key, value)
    s.commit()
    serialized_order = OrderSchema().dump(order)
    return jsonify(serialized_order)


@api_blueprint.route('/user/login', methods=['POST'])
def login():
    json_user_data = request.get_json()
    if not json_user_data:
        return {"message": "Empty request body"}, 400

    user_find = s.query(User).filter_by(name=json_user_data['username']).first()
    if not user_find:
        return {"message": "User with such username does not exists"}, 404

    if not Bcrypt().check_password_hash(user_find.password, json_user_data['password']):
        return {"message": "Provided credentials are invalid"}, 400

    serialized_user = UserSchema().dump(user_find)
    return jsonify(serialized_user)
