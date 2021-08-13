from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import Employee
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


emp = Blueprint('emp', __name__, url_prefix='/emp')


@emp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("user email",email)
        em=Employee.query.all()
        print(em)
        #print(em[0][0])
        #print(em[0].Email)
        for emp in em:
            print(emp.email)
        employee = Employee.query.filter_by(email=email).first()
        print(employee)
        if employee:
            if(employee.password is None):
                flash('New Employee- Sign Up first',category='info')
                #return redirect(url_for('emp.sign_up'))
                return render_template("employee/esignup.html")
            elif check_password_hash(employee.password, password):
                flash('Logged in successfully!', category='success')
                login_user(employee)
               # return redirect(url_for('views.home'))
                return render_template("employee/ebase.html")
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("employee/elogin.html", user=current_user)


@emp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully',category='success')
    return redirect(url_for('emp.login'))


@emp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        id= request.form.get('id')
        email = request.form.get('email')
        #first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        employee = Employee.query.filter_by(employee_id=id).first()
        if employee:
            if (employee.email == email):
                if(employee.password is None):
                    if password1 != password2:
                        flash('Passwords don\'t match.',category='error')
                    else:
                        setattr(employee, 'password', generate_password_hash(password1, method='sha256'))
                        db.session.commit()
                        login_user(employee)
                        flash('Welcome to Idiogai Shop!!!!!!!!!',category='success')
                        return render_template("employee/ebase.html")
                else:
                    flash('password already there, please signin with set password',category='error')
            else:
                flash('email is not correct. try again',category='error')
        else:
            flash('No employee found on this id number',category='error')
          
    return render_template("employee/esignup.html", user=current_user)
