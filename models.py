from sqlalchemy import ForeignKey, INTEGER, Column, String, Enum, Boolean, DateTime, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
engine = create_engine("mysql+pymysql://root:password@localhost:3306/api_db", echo=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    username = Column(String(45), nullable=False)
    name = Column(String(45), nullable=False)
    second_name = Column(String(45), nullable=False)
    password = Column(String(180), nullable=False)
    role = Column(Enum('admin', 'customer'))

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.name}, {self.second_name}, {self.password}, " \
               f"{self.role_id}"


class Order(Base):
    __tablename__ = 'order'
    id = Column(INTEGER, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_complete = Column(Boolean, nullable=False)
    user_id = Column(INTEGER, ForeignKey('user.id'))
    user = relationship("User")
    car_id = Column(INTEGER, ForeignKey('car.id'))
    car = relationship("Car")

    def __repr__(self):
        return f"{self.id}, {self.start_date}, {self.end_date}, {self.is_complete}, {self.user_id}"


class Car(Base):
    __tablename__ = 'car'
    id = Column(INTEGER, primary_key=True)
    model = Column(String(45), nullable=False)
    brand = Column(String(45), nullable=False)
    status = Column(Enum('available', 'reserved'))
    price = Column(INTEGER, nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.model}, {self.brand}, {self.status}, {self.price}"
