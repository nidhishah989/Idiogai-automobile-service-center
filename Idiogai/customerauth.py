from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


cus = Blueprint('cus', __name__,)


@cus.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
       
        customer = Customer.query.filter_by(email=email).first()
        
        if customer:
            if(customer.password is None):
                flash('New Customer- Let\'s Sign Up you first',category='info')
                return redirect(url_for('cus.sign_up'))
               # return render_template("cust/esignup.html")
            elif check_password_hash(customer.password, password):
                flash('Logged in successfully!', category='success')
                login_user(customer)
               # return redirect(url_for('views.home'))
                return render_template("customer/ubase.html")
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("customer/custlogin.html", user=current_user)


@cus.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully',category='success')
    return redirect(url_for('cus.login'))


@cus.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        
        email = request.form.get('email')
        #first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        customer = Customer.query.filter_by(email=email).first()
        if customer:
                if(customer.password is None):
                    if password1 != password2:
                        flash('Passwords don\'t match.',category='error')
                    else:
                        setattr(customer, 'password', generate_password_hash(password1, method='sha256'))
                        db.session.commit()
                        login_user(customer)
                        flash('Welcome to Idiogai Shop!!!!!!!!!',category='success')
                        return render_template("customer/ubase.html")
                else:
                    flash('password already there, please signin with set password',category='error')
        else:
            flash('email is not correct. try again',category='error')
        
          
    return render_template("customer/custsignup.html", user=current_user)
