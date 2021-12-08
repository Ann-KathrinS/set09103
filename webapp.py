from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

"Database"

db_location = 'var/sqlite3.db'

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()    


@app.route('/test')
def test():
    return render_template('petTile.html'),200

@app.route('/')
def root():
    return render_template('index.html'),200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

@app.route('/pet-added')
def petAdded():
    return render_template('petAdded.html'),200


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
