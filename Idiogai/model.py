from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Customer(db.Model,UserMixin):
    customer_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(45))
    phone=db.Column(db.String(10))
    Email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    address=db.Column(db.String(250))
    city=db.Column(db.String(100))
    state=db.Column(db.String(100))
    country=db.Column(db.String(100))
    zipcode=db.Column(db.Integer())
    vehicles=db.relationship('Vehicle')
    cust_plans=db.relationship('Customizationdetail')

class Employee(db.Model,UserMixin):
    employee_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(45))
    jobtitle=db.Column(db.String(200))
    phone=db.Column(db.String(10))
    Email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    address=db.Column(db.String(250))
    city=db.Column(db.String(100))
    state=db.Column(db.String(100))
    country=db.Column(db.String(100))
    zipcode=db.Column(db.Integer())
    cust_resp=db.relationship('Customizationdetail')
    items=db.relationship('Item')
    usedinitems=db.relationship('Labordetail')

class Vehicle(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    vin=db.Column(db.String(200),unique=True)
    mkae=db.Column(db.String(200))
    model=db.Column(db.String(200))
    engine=db.Column(db.String(200))
    trim=db.Column(db.String(200))
    interior=db.Column(db.String(200))
    exterior=db.Column(db.String(200))
    bodyCondition=db.Column(db.String(200))
    frameCondition=db.Column(db.String(200))
    interiorCondition=db.Column(db.String(200))
    engineCondition=db.Column(db.String(200))
    cust_id=db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    custom_plans=db.relationship('Customizationdetail')

class Customizationplan(db.Model):
    plan_id=db.Column(db.Integer(),primary_key=True)
    total_Estimated_price=db.Column(db.Float())
    deposited_amount=db.Column(db.Float())
    subtotal_price=db.Column(db.Float())
    tax_amount=db.Column(db.Float())
    amount_due=db.Column(db.Float())
    startdate=db.Column(db.DateTime(timezone=True))
    estimated_delivery_date=db.Column(db.DateTime(timezone=True))
    payment_date=db.Column(db.DateTime(timezone=True))
    payment_method=db.Column(db.String(100))
    cust_details=db.relationship('Customizationdetail',uselist=False)
    items=db.relationship('Item')
    questions=db.relationship('questions')

class Customizationdetail(db.Model):
    pl_id=db.Column(db.Integer(),db.ForeignKey('customizationplan.plan_id'),primary_key=True)
    cus_id=db.Column(db.Integer(), db.ForeignKey('customer.customer_id'))
    vin_id=db.Column(db.Integer(),db.ForeignKey('vehicle.id'))
    emp_id=db.Column(db.Integer(),db.ForeignKey('employee.employee_id'))

class Item(db.Model):
    item_id=db.Column(db.Integer(),primary_key=True)
    item_name=db.Column(db.String(200))
    item_description=db.Column(db.String(1000))
    item_estimated_price=db.Column(db.Float())
    item_completion_estimation=db.Column(db.DateTime(timezone=True))
    item_actual_part_cost=db.Column(db.Float())
    item_actual_labor_cost=db.Column(db.Float())
    pln_id=db.Column(db.Integer(),db.ForeignKey('customizationplan.plan_id'))
    empl_id=db.Column(db.Integer(),db.ForeignKey('employee.employee_id'))
    parts=db.relationship('Partdetail')
    labors=db.relationship('Labordetail')

class part(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    part_price=db.Column(db.Float())
    part_manufacture=db.Column(db.String(200))
    usedinitems=db.relationship('Partdetail')

class Partdetail(db.Model):
    p_id=db.Column(db.Integer(),db.ForeignKey('part.id'),primary_key=True,unique=False)
    it_id=db.Column(db.Integer(),db.ForeignKey('item.item_id'),primary_key=True,unique=False)
    part_quantity=db.Column(db.Integer())
    part_total_cost=db.Column(db.Float())

class labor(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    labor_cost=db.Column(db.Float())
    labor_description=db.Column(db.String(200))
    usedinitems=db.relationship('Labordetail')

class Labordetail(db.Model):
    l_id=db.Column(db.Integer(),db.ForeignKey('labor.id'),primary_key=True,unique=False)
    it_id=db.Column(db.Integer(),db.ForeignKey('item.item_id'),primary_key=True,unique=False)
    labor_time=db.Column(db.Float())
    labor_total_cost=db.Column(db.Float())
    labor_employee=db.Column(db.Integer(),db.ForeignKey('employee.employee_id'))

class questions(db.Model):
    plan = db.Column(db.Integer(),db.ForeignKey('customizationplan.plan_id'),primary_key=True,unique=False)
    question_num=db.Column(db.Integer(),primary_key=True,unique=False)
    question_date = db.Column(db.DateTime(timezone=True), default=func.now())
    question=db.Column(db.String(1000))
    answer=db.Column(db.String(10000))