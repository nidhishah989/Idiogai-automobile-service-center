#This is the file that makes the Idiogai directory as application package
#this file is setup for application basic setting such as path and application factory.
#source :link: https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
##################################
#now first import the required modules.
#os for operating system functions
#Flask to create a instance of Flask to create application
import os
from flask import Flask
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
    #instance folder outside of this folder
    app = Flask(__name__,instance_relative_config=True)
    #from_mapping set some default configuration 
    app.config.from_mapping(
        #to keep data safe, secret key is require, 
        #however, change it to random string before deployment of this application
        SeCRET_KEY='dev',
        #this provides the path to the database named: Sqlite
        #as mention before the database files will in instance folder.So instance_path
        DATABASE=os.path.join(app.instance_path,'Idiogai.sqlite'),
    )

    #now here is two things, the application input is test or actual runnig app with client
    #it will be checked with test_config variable.
    #if is not test_config, then use config file if exits in instace folder for configuratio of app
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # this is to override above default config setting
        #in the config.py you can set secret key
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    #flask does not create instance folder automatically. you have to create using this line of code
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello/')
    def hello():
        return 'Hello, World!'

    return app