import os
from xmlrpc.client import DateTime
from flask import Flask, redirect, render_template, request
from .lookup import reddit_lookup
import datetime
import sqlite3



def create_app(test_config=None):
    
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

   
    @app.route('/users', methods = ['GET','POST'])
    def users():
        con = sqlite3.connect('mooddit.db')
        db = con.cursor()
        
        pos_result = ()
        neg_result = ()

        # Select top comments by pos
        pos_query = "SELECT name, compound FROM user ORDER BY compound DESC limit 5"

        # Select top comments by neg\
        neg_query = "SELECT name, compound FROM user ORDER BY compound ASC limit 5"

        db.execute(pos_query)
        result = db.fetchall()
        pos_result = result
        
        db.execute(neg_query)
        result = db.fetchall()
        neg_result = result
        
        db.close()
        return render_template('users.html', pos_result = pos_result, neg_result = neg_result)
    
    @app.route('/subreddits', methods = ['GET','POST'])
    def subreddits():
        con = sqlite3.connect('mooddit.db')
        db = con.cursor()

        pos_result = ()
        neg_result = ()

        # Select top comments by pos
        pos_query = "SELECT name, compound FROM subreddit ORDER BY compound DESC limit 4"

        # Select top comments by neg\
        neg_query = "SELECT name, compound FROM subreddit ORDER BY compound ASC limit 4"

        db.execute(pos_query)
        result = db.fetchall()
        pos_result = result
        
        db.execute(neg_query)
        result = db.fetchall()
        neg_result = result

        db.close
        return render_template('subreddits.html', pos_result = pos_result, neg_result = neg_result)

    @app.route('/', methods = ["GET","POST"])
    def index():

            return render_template("home.html")
    
    @app.route('/search', methods = ['GET', 'POST'])
    def search():

        # Create sqlite3 database
        con = sqlite3.connect('mooddit.db')
        db = con.cursor()
        

        #Set up POST actions
        if request.method == "POST":

            # Get user input from form
            userinput = request.form.get("userinput")
            inp_type = userinput[:3]
            inp_value = userinput[3:]

            #check first 3 chars to determin if it's a user or a subreddit, set new value
            if inp_type == '/u/':
                inp_type = 'user'
            elif inp_type == '/r/':
                inp_type = 'subreddit'
            else:
                msg = "include /u/ or /r/"
                return render_template("search.html", msg = msg)
            
            # Check to see if there's already sentiment data stored in the database. 
            # It will return much faster than using the reddit api
            check_query = f"SELECT pos,neu,neg,compound FROM {inp_type} WHERE name = '{inp_value}'"
            db.execute(check_query)
            result = db.fetchall()

            # Convert the SQL results into dict data format
            if result:
                data = {
                    'pos':result[0][0],
                    'neu':result[0][1],
                    'neg':result[0][2],
                    'compound':result[0][3]
                }
                # Evaluate user message. Better implementation somehow?
                eval = ""
                x = result[0][3]
                if x <= .05 and x >= -.05:
                    eval = "Neutral"
                elif x > .05 and x < .25:
                    eval = "Somewhat Positive"
                elif x > .25:
                    eval = "Extemely Positive"
                elif x > -.25 and x < -.05:
                    eval = "Somewhat Negative"
                elif x < -.25:
                    eval = "Extremely Negative"

                #end the function right here if we have a result from the db
                return render_template("results.html", data = data, eval = eval, inp_type = inp_type, inp_value = inp_value)

            # call lookup function to get reddit sentiment data
            data = reddit_lookup(inp_value, inp_type)
        
            if "404" in data:
                msg = ""
                if "user" in data:
                    msg = "user not found"
                elif "subreddit" in data:
                    msg = "subreddit not found"
                return render_template("search.html", msg = msg)

            # Evaluate user message. Better implementation somehow?
            eval = ""
            x = data['compound']
            if x <= .05 and x >= -.05:
                eval = "Neutral"
            elif x > .05 and x < .2:
                eval = "Somewhat Positive"
            elif x > .2:
                eval = "Extemely Positive"
            elif x > -.2 and x < -.05:
                eval = "Somewhat Negative"
            elif x < -.2:
                eval = "Extremely Negative"

            
            #insert lookup data into the database
            query = f"INSERT INTO {inp_type} (name, pos, neg, neu, compound, date_added) VALUES ('{inp_value}',{data['pos']},{data['neg']},{data['neu']}, {data['compound']},'{datetime.datetime.now()}')"    
           
            #execute Insert query
            db.execute(query)
           
            # close DB
            con.commit()
            db.close()

            #return results and display the reddit data
            return render_template("results.html", data = data, eval = eval, inp_type = inp_type, inp_value = inp_value)
        else:
            return render_template('search.html')
        
        
    
    return app

