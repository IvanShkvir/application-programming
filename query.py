from sqlalchemy.orm import sessionmaker
from models import *

session = sessionmaker(bind=engine)
s = session()

new_role = Role(id=1, role_name='dasasd')
new_user = User(id=1, username='faferfs', name='fdsfef', second_name='gkfdfsfd', password='akdskmamk', role_id=1)
new_order = Order(id=1, start_date="2003-10-23 10:10:10", end_date="2003-10-23 10:12:10", is_complete=True, user_id=1)
new_car = Car(id=1, model='dmaskam', brand='eforkeokf', status=StatusEnum.reserved, price=1000)
new_order_car = Order_Car(order_id=1, car_id=1)

s.add(new_role)
s.add(new_car)
s.add(new_user)
s.add(new_order)
s.add(new_order_car)
s.commit()

