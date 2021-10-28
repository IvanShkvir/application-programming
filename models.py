from sqlalchemy import ForeignKey, INTEGER, Column, String, Enum, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config import username, password, server
from enums import StatusEnum

Base = declarative_base()
engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{server}/api_db", echo=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    username = Column(String(45), nullable=False)
    name = Column(String(45), nullable=False)
    second_name = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
    role_id = Column(INTEGER, ForeignKey('role.id'))
    role = relationship("Role")

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.name}, {self.second_name}, {self.password}, " \
               f"{self.role_id}"


class Role(Base):
    __tablename__ = 'role'
    id = Column(INTEGER, primary_key=True)
    role_name = Column(String(45), nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.role_name}"


class Order_Car(Base):
    __tablename__ = 'order_car'
    order_id = Column(INTEGER, ForeignKey("order.id"), primary_key=True)
    car_id = Column(INTEGER, ForeignKey("car.id"), primary_key=True)
    order = relationship("Order")
    car = relationship("Car")

    def __repr__(self):
        return f"{self.order_id},{self.car_id}"


class Order(Base):
    __tablename__ = 'order'
    id = Column(INTEGER, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_complete = Column(Boolean, nullable=False)
    user_id = Column(INTEGER, ForeignKey('user.id'))
    user = relationship("User")
    # car = relationship('Order', secondary=Order_Car, backref='order')

    def __repr__(self):
        return f"{self.id}, {self.start_date}, {self.end_date}, {self.is_complete}, {self.user_id}"


class Car(Base):
    __tablename__ = 'car'
    id = Column(INTEGER, primary_key=True)
    model = Column(String(45), nullable=False)
    brand = Column(String(45), nullable=False)
    status = Column(Enum(StatusEnum))
    price = Column(INTEGER, nullable=False)
    # order = relationship('Car', secondary=Order_Car, backref='car')

    def __repr__(self):
        return f"{self.id}, {self.model}, {self.brand}, {self.status}, {self.price}"


# Base.metadata.create_all(engine)
