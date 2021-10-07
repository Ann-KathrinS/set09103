from flask import Flask, redirect, url_for, abort
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Napier"


@app.route("/private")
def private():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return "Now we would get username & password"

@app.errorhandler(404)
def page_not_found(error):
    return """Couldn't find the page you requested.
            <a href='http://webtech-48.napier.ac.uk:5000'>Click here to go back</a>


    """, 404

@app.errorhandler(401)
def page_moved(error):
    return """This page was moved. You can find it 
            <a href='http://webtech-48.napier.ac.uk/login'>here</a>""", 401

@app.route('/force401')
def force401():
    abort(401)


@app.route('/force404')
def force404():
    abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
