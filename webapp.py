from flask import Flask, render_template, g, request, url_for, flash, redirect
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



@app.route('/')
def root():
    return render_template('index.html'),200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

@app.route('/pet-added', methods=['POST'])
def petAdded():
    if request.method == 'POST':
        reportType = request.form['reportType']
        petType = request.form['petType']
        otherPetType = request.form['otherPetType']
        petName = request.form['petName']
        postcode = request.form['postcode']
        if reportType == 'missing':
            date = request.form['missingDate']
        else:
            date = request.form['foundDate']
        petAge = request.form['petAge']
        colourBlack = request.form['black']
        colourWhite = request.form['white']
        colourBrown = request.form['brown']


    return render_template('petAdded.html'),200

@app.route('/report-missing-pet' methods=('GET', 'POST'))
def report_missing():
    return render_template('reportMissing.html'),200

@app.route('/report-found-pet' methods=('GET', 'POST'))
def report_found():
    return render_template('reportFound.html'),200

@app.route('/missing' methods=('GET', 'POST'))
def showMissing():
    return render_template('petTile.html'),200

@app.route('/found' methods=('GET', 'POST'))
def showFound():
    return render_template('petTile.html'),200

@app.route('/missing/<petId>/<petName>' methods=('GET', 'POST'))
def missingPet():
    return render_template('comment.html'),200

@app.route('/found/<petId>/<petName>' methods=('GET', 'POST'))
def foundPet():
    return render_template('comment.html'),200

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
