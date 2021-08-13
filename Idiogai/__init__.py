#This is the file that makes the Idiogai directory as application package
#this file is setup for application basic setting such as path and application factory.
#source :link: https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
##################################
#now first import the required modules.
#os for operating system functions
#Flask to create a instance of Flask to create application
#Flasksqlalchemy for Sqlalchemy to connect with database and do database queries using this ORM
#flask_login to support customer and employee login functions
#click and flask.cli to support database initialization
import os
from os import path
import click
from flask import Flask,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.cli import with_appcontext

##################################
# Now, let set database first
db=SQLAlchemy()
##################################
# Now set the required settigns of application
# first: set application factory. 
#look into the link above to see other links related to factory function parts
#here, the factory function name is create_app

def create_app(test_config =None):
    #create an instance of Flask as app 
    #link to each part of creating app is in the above link
    #__name__used to tell app that current module is the location to set up some paths
    #instance_relative_config=True means the configuration files and database files are in the
    # for this application, we are not creating database file, but for future. might need
    #instance folder outside of this folder
    app = Flask(__name__,instance_relative_config=True)
    #from_mapping set some default configuration 
    app.config.from_mapping(
        #to keep data safe, secret key is require, 
        #however, change it to random string before deployment of this application
        SECRET_KEY='dev',

        #connect the database engine here. #make sure you have database idiogai created locally before creating app
        SQLALCHEMY_DATABASE_URI = 'mysql://root:root1234@localhost/Idiogai',
        
    )

    db.init_app(app)

    ##################################################################################
    ########################### REGISTER BLUEPRINTS ################################
    from . import employee # register auth blueprint
    app.register_blueprint(employee.emp)

    from .import customerauth
    app.register_blueprint(customerauth.cus)
    ###################################################################################
    ########################################### Database table setting #######################################
    # call the command from cmd line to initialize the database tables.
    #we are not droping the table if created to update the table, so need to drop manually, either by mysql workbench or shell
    # in command promt run: flask init-db
    # this will call function and create tables that does not exist in database.
    #again to update table, drop it first manually before passing this command in command prompt
    # you need to call all tables here, otherwise the create_all() function will not add any table 
    from .model import Customer,Employee,Vehicle,Customizationplan,Customizationdetail,part,Partdetail,Item,labor,Labordetail
    app.cli.add_command(init_db_command)

    ##################################################################################################################
    #now here is two things, the application input is test or actual runnig app with client
    #it will be checked with test_config variable.
    #if is not test_config, then use config file if exits in instace folder for configuratio of app
    ################# if Test_config is not called ########################################
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # this is to override above default config setting
        #in the config.py you can set secret key
        app.config.from_pyfile('config.py', silent=True)
     ####################################### if Test_config is called #######################
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    ##############################################################################################################
    # ensure the instance folder exists
    #flask does not create instance folder automatically. you have to create using this line of code
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    ##############################################################################################
    # a simple page that says hello
    @app.route('/hello/')
    def hello():
        return 'Hello, World!'
    ########################################################################################
    login_manager = LoginManager()
    login_manager.login_view = 'emp.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(employee_id):
        return Employee.query.get(employee_id)

    @login_manager.user_loader
    def load_user(customer_id):
        return Customer.query.get(customer_id)
    ############################################################################################
    return app
    
####################################### database table-initialize-cmd-function #############
# this function is called to initialize the tables.
# check comments for 
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all(app=current_app)
    # send a message in cmd window
    click.echo('Initialized the database.')
##########################################################################################