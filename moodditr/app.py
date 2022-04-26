import os
from flask import Flask, render_template, request
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
    def hello():
        
        if request.method == "POST":
            username = request.form.get("user")
            print(username)
            return render_template("test.html", username = username)
        else:
            return render_template("base.html")
    
    from . import db
    db.init_app(app)
    return app
