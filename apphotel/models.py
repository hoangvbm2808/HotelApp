import hashlib
from enum import Enum as UserEnum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from apphotel import db, app


class UserRole(UserEnum):
    RECEP = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class TypeRoom(BaseModel):
    name = Column(String(100), nullable=False)
    room = relationship('Room', backref='typeRoom', lazy=False)

    def __str__(self):
        return self.name


class Room(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    max = Column(Integer, default=0)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now())
    TypeRoom_id = Column(Integer, ForeignKey(TypeRoom.id), nullable=False)

    def __str__(self):
        return self.name


# class User(BaseModel):
#     name = Column(String(50), nullable=False)
#     username = Column(String(50), nullable=False, unique=True)
#     password = Column(String(50), nullable=False)
#
#     def __str__(self):
#         return self.name


class Account(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    # avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.RECEP)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = Column(String(500), nullable=False)
    country = Column(String(500), nullable=False)
    citizen_id = Column(String(500), nullable=False)
    address = Column(String(500),  nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)

    def __str__(self):
        return self.name


class BookingForm(BaseModel):
    Room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    DayBook = Column(DateTime, default=datetime.now())
    Check_inDate = Column(DateTime, default=DayBook)
    # (Check_inDate - DayBook).days
    Check_outDay = Column(DateTime)
    Room_name = Column(String(50), nullable=False)
    Customer_name1 = Column(String(50), nullable=False)
    Customer_name2 = Column(String(50), nullable=True)
    Customer_name3 = Column(String(50), nullable=True)
    Customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)

    def __str__(self):
        return self.idForm


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        p1 = TypeRoom(name='Standard')
        p2 = TypeRoom(name='Deluxe')
        p3 = TypeRoom(name='Suite')
        db.session.add_all([p1, p2, p3])
        db.session.commit()

        c1 = Room(name='Phòng 101', description='Giường đơn', price=300000, max=2, image='images/p1.jpg', TypeRoom_id=1)
        c2 = Room(name='Phòng 102', description='Giường đôi', price=500000, max=3, image='images/p2.jpg', TypeRoom_id=1)
        c3 = Room(name='Phòng 103', description='Giường đôi', price=700000, max=3, image='images/p3.jpg', TypeRoom_id=1)
        c4 = Room(name='Phòng 104', description='Giường đơn', price=300000, max=2, image='images/p4.jpg', TypeRoom_id=1)
        c5 = Room(name='Phòng 105', description='Giường đơn', price=300000, max=2, image='images/p5.jpg', TypeRoom_id=1)
        c6 = Room(name='Phòng 106', description='Giường đôi', price=3800000, max=3, image='images/p6.jpg', TypeRoom_id=1)
        c7 = Room(name='Phòng 201', description='Giường đôi', price=1300000, max=3, image='images/p1.jpg', TypeRoom_id=2)
        c8 = Room(name='Phòng 202', description='Giường đơn', price=2000000, max=2, image='images/p2.jpg', TypeRoom_id=2)
        c9 = Room(name='Phòng 203', description='Giường đôi', price=300000, max=3, image='images/p3.jpg', TypeRoom_id=2)
        c10 = Room(name='Phòng 204', description='Giường đôi', price=3500000, max=3, image='images/p4.jpg', TypeRoom_id=2)
        c11 = Room(name='Phòng 205', description='Giường đơn', price=3200000, max=2, image='images/p5.jpg', TypeRoom_id=2)
        c12 = Room(name='Phòng 206', description='Giường đôi', price=3100000, max=3, image='images/p6.jpg', TypeRoom_id=2)
        c13 = Room(name='Phòng 301', description='Giường đơn', price=2200000, max=2, image='images/p1.jpg', TypeRoom_id=3)
        c14 = Room(name='Phòng 302', description='Giường đôi', price=400000, max=3, image='images/p2.jpg', TypeRoom_id=3)
        c15 = Room(name='Phòng 303', description='Giường đơn', price=3000000, max=2, image='images/p3.jpg', TypeRoom_id=3)
        c16 = Room(name='Phòng 304', description='Giường đơn', price=2300000, max=2, image='images/p4.jpg', TypeRoom_id=3)
        c17 = Room(name='Phòng 305', description='Giường đôi', price=1300000, max=3, image='images/p5.jpg', TypeRoom_id=3)
        c18 = Room(name='Phòng 306', description='Giường đôi', price=3000000, max=3, image='images/p6.jpg', TypeRoom_id=3)
        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18])
        db.session.commit()

        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        a1 = Account(name='Thuyền', username='thuyen123', password=password)
        a2 = Account(name='Ân', username='an123', password=password, user_role=UserRole.ADMIN)

        db.session.add_all([a1, a2])
        db.session.commit()
        # db.create_all()
