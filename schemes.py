from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    name = fields.Str()
    second_name = fields.Str()
    password = fields.Str()
    role = fields.String(validate=validate.OneOf(["admin", "customer"]))


class CarSchema(Schema):
    id = fields.Int()
    model = fields.Str()
    brand = fields.Str()
    status = fields.Str(validate=validate.OneOf(["reserved", "available"]))
    price = fields.Int()
    image = fields.Str()


class OrderSchema(Schema):
    id = fields.Int()
    start_date = fields.Date()
    end_date = fields.Date()
    is_complete = fields.Boolean()
    user_id = fields.Int()
    car_id = fields.Int()
