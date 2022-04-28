from cgitb import lookup
import os
from flask import Flask, redirect, render_template, request
from .lookup import reddit_lookup


def create_app(test_config=None):
    # create and configure the app

    # create flask instance 
    app = Flask(__name__, instance_relative_config=True)

    # set default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path, 'mooddit.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent = True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # helloworld page
    
    
    @app.route('/', methods = ["GET","POST"])
    def index():
        if request.method == "POST":
            # Get user input from form
            userinput = request.form.get("userinput")
            inp_type = userinput[:3]
            inp_value = userinput[3:]
            #check first 3 chars to determin if it's a user or a subreddit
            if userinput[:3] != '/u/' and userinput[:3] != '/r/':
                
                return "first 3 chars incorrect"
            
            # call lookup function to get reddit sentiment data
            # first 3 chars describe type, everything ekse is the search query
            data = reddit_lookup(inp_value, inp_type)
            print("data:",data)
            #return results and display the reddit data
            return render_template("results.html", data = data)

        else:
            return render_template("home.html")
   
    
    from . import db
    db.init_app(app)

    @app.route('/results', methods = ['GET', 'POST'])
    def results():
        print("ASdfasdf")
        return 0
    return app
