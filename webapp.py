from flask import Flask, render_template, g, request, url_for, flash, redirect
import sqlite3
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER']="static/img"

#Database

#db_location = 'var/sqlite3.db'
db_location = 'var/pets.db'

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
        colourBlack = request.form.get('black')
        colourWhite = request.form.get('white')
        colourBrown = request.form.get('brown')
        colourLightBrown = request.form.get('lightBrown')
        colourGrey = request.form.get('grey')
        colourBeige = request.form.get('beige')
        colourRed = request.form.get('red')
        colourOther = request.form.get('other')
        otherColours = request.form['othercolours']
        sex = request.form['sex']
        description = request.form['petDescription']
        #petPhoto = request.form['petPhoto']
        ownersName = request.form['ownersName']
        email = request.form['email']
        ownersSurname = request.form['ownersSurname']

        petPhoto = request.files['petPhoto']
        if petPhoto.filename != '':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], petPhoto.filename)
            petPhoto.save(filepath)

        #Split postcode into area and incod
        postcodeCharacters = list(postcode)
        postcodeIncode = ""
        postcodeArea = ""

        postcodeIncode = postcodeIncode + postcodeCharacters[len(postcodeCharacters)-3]
        postcodeIncode = postcodeIncode + postcodeCharacters[len(postcodeCharacters)-2]
        postcodeIncode = postcodeIncode + postcodeCharacters[len(postcodeCharacters)-1]

        del postcodeCharacters[len(postcodeCharacters)-3]
        del postcodeCharacters[len(postcodeCharacters)-2]
        del postcodeCharacters[len(postcodeCharacters)-1]

        for character in postcodeCharacters:
            postcodeArea = postcodeArea + character

        
        
        
        db = get_db()
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('INSERT INTO pet (reportType, petType, name, reportDate, postcodeArea, postcodeIncode, age, sex, description, photo, ownerName, ownerSurname, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (reportType, petType, petName, date, postcodeArea, postcodeIncode, petAge, sex, description, petPhoto.filename, ownersName, ownersSurname, email))
        db.commit()
       # petId = db.cursor().execute('SELECT last_insert_rowid()')
        petId = cursor.lastrowid
       
        if colourBlack == "on":
            cursor.execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId,'1'))
            db.commit()

        if colourWhite == "on":
            cursor.execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId, '2'))
            db.commit()

        if colourBrown == "on":
           db.cursor().execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId, '3'))
           db.commit()

        if colourLightBrown == "on":
            cursor.execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId, '4'))
            db.commit()

        if colourGrey == "on":
            cursor.execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId, '5'))
            
            db.commit()
        if colourBeige == "on":
            cursor.execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId, '6'))
            db.commit()
        if colourRed == "on":
            cursor.execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId, '7'))
            db.commit()

        if colourOther == "on":
            cursor.execute('INSERT INTO colour (category, name) VALUES (?, ?)', (other, otherColours))

            db.commit()
            colourId = db.cursor().execute('SELECT last_insert_rowid()')
            cursor.execute('INSERT INTO petColour (petId, colourId) VALUES (?, ?)', (petId, colourId))

        db.commit()

        #sql = "SELECT petId FROM pet WHERE petId=?"
        #pet = cursor.execute(sql, [petId]).fetchall()

        pet = cursor.execute("SELECT * FROM pet WHERE petId=?", (petId,)).fetchone()
        #page = []
        #page.append('<html><p>')
        #page.append(str(pet))
        #page.append('</p></html>')
        #return ''.join(page)
   
        
        if reportType == "missing":
            return render_template('textAddMissing.html', pet=pet),200
        else:
            return render_template('textAddFound.html', pet=pet),200
    
       

@app.route('/report-missing-pet', methods=('GET', 'POST'))
def report_missing():
    return render_template('reportMissing.html'),200

@app.route('/report-found-pet', methods=('GET', 'POST'))
def report_found():
    return render_template('reportFound.html'),200

@app.route('/missing', methods=('GET', 'POST'))
def showMissing():
    return render_template('petTile.html'),200

@app.route('/found', methods=('GET', 'POST'))
def showFound():
    return render_template('petTile.html'),200

@app.route('/missing/<petId>/<petName>', methods=('GET', 'POST'))
def missingPet(petId,petName):

    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()

    pet = cursor.execute("SELECT * FROM pet WHERE petId=?", (petId,)).fetchone()
  


    return render_template('comment.html', pet=pet),200

@app.route('/found/<petId>/<petName>', methods=('GET', 'POST'))
def foundPet():
    return render_template('comment.html'),200

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
