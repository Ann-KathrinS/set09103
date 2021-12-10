from flask import Flask, render_template, g, request, url_for, flash, redirect
import sqlite3
import os
from jinjasql import JinjaSql

j = JinjaSql()

app = Flask(__name__)

app.config['UPLOAD_FOLDER']="static/img"

#sql template
template = """
    SELECT * FROM pet
    WHERE reportType = {{ reportType }}
    {% if not petType == '' %}
    AND petType = {{ petType }}
    {% endif %}
    {% if not postcodeArea == 'Filter location' %}
    AND postcodeArea = {{ postcodeArea }}
    {% endif %}
    {% if not black == '' %}
    AND black = 1
    {% endif %}
    {% if not white == '' %}
    AND white = 1
    {% endif %}
    {% if not brown == '' %}
    AND brown = 1
    {% endif %}
    {% if not white == '' %}
    AND white = 1
    {% endif %}
    {% if not lightBrown == '' %}
    AND lightBrown = 1
    {% endif %}
    {% if not grey == '' %}
    AND grey = 1
    {% endif %}
    {% if not beige == '' %}
    AND beige = 1
    {% endif %}
    {% if not red == '' %}
    AND red = 1
    {% endif %}
    {% if not other == '' %}
    AND other = 1
    {% endif %}
"""    


#Database

#db_location = 'var/sqlite3.db'
db_location = 'var/pets22.db'

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
        if reportType == 'Missing':
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

       
        if colourBlack == "on":
            black = 1
        else:
            black = 0

        if colourWhite == "on":
            white = 1
        else:
            white = 0

        if colourBrown == "on":
            brown = 1
        else:
            brown = 0 
            
        if colourLightBrown == "on":
            lightBrown = 1
        else:
            lightBrown = 0
           
        if colourGrey == "on":
            grey = 1
        else:
            grey = 0
         
        if colourBeige == "on":
            beige = 1
        else:
            beige = 0
            
        if colourRed == "on":
            red = 1
        else:
            red = 0
            
        if colourOther == "on":
            other = 1
        else:
            other = 0
        

        db = get_db()
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('INSERT INTO pet (reportType, petType, otherPetType, name, reportDate, postcodeArea, postcodeIncode, age, sex, description, photo, ownerName, ownerSurname, email, black, white, brown, lightBrown, grey, beige, red, other, otherColour) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (reportType, otherPetType, petType, petName, date, postcodeArea, postcodeIncode, petAge, sex, description, petPhoto.filename, ownersName, ownersSurname, email, black, white, brown, lightBrown, grey, beige, red, other, otherColours))
        db.commit()

        petId = cursor.lastrowid

        pet = cursor.execute("SELECT * FROM pet WHERE pet.petId =?", (petId ,)).fetchone()
        #page = []
        #page.append('<html><p>')
        #page.append(str(pet))
        #page.append('</p></html>')
        #return ''.join(page)
   
        
        if reportType == "Missing":
            return render_template('textAddMissing.html', pet=pet, reportType="Missing" ),200
        else:
            return render_template('textAddFound.html', pet=pet, reportType="Found"),200
        
       

@app.route('/report-missing-pet', methods=('GET', 'POST'))
def report_missing():
    return render_template('reportMissing.html'),200

@app.route('/report-found-pet', methods=('GET', 'POST'))
def report_found():
    return render_template('reportFound.html'),200

@app.route('/missing', methods=('GET', 'POST'))
def showMissing():

    #Try filter options (doesn't work)
    """if request.method == 'POST':
        petType = request.form['petType']
        postcodeArea = request.form['location']
        colourBlack = request.form.get('black')
        colourWhite = request.form.get('white')
        colourBrown = request.form.get('brown')
        colourLightBrown = request.form.get('lightBrown')
        colourGrey = request.form.get('grey')
        colourBeige = request.form.get('beige')
        colourRed = request.form.get('red')
        colourOther = request.form.get('other')
        sex = request.form.get('sex')


        #prepare data for sql query

        data = {
                "reportType": "Found",
                "petType": petType,
                "postcodeArea": postcodeArea,
                #"sex": sex,
                "black": colourBlack,
                "white": colourWhite,
                "brown": colourBrown,
                "lightBrown": colourLightBrown,
                "grey": colourGrey,
                "beige": colourBeige,
                "red": colourRed,
                "other": colourOther
                }


        query, bind_params = j.prepare_query(template, data)

        #self.assertEquals(bind_params, [reportType, petType, postcodeArea, sex, colourBlack, colourWhite, colourBrown, colourLightBrown, colourGrey, colourBeige,colourRed, colourOther])

        #self.assertEquals(query.strip(), expected_query.strip())

        db = get_db()
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        pets = cursor.execute(query, (bind_params)).fetchall()

    else:"""


    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()

    reportType = "Missing"

    pets = cursor.execute("SELECT * FROM pet WHERE reportType=?", (reportType,)).fetchall()

    return render_template('pagePets.html', pets=pets, reportType=reportType),200

@app.route('/found', methods=('GET', 'POST'))
def showFound():
    

    #Try filter options (doesn't work)
    """if request.method == 'POST':
        petType = request.form['petType']
        postcodeArea = request.form['location']
        colourBlack = request.form.get('black')
        colourWhite = request.form.get('white')
        colourBrown = request.form.get('brown')
        colourLightBrown = request.form.get('lightBrown')
        colourGrey = request.form.get('grey')
        colourBeige = request.form.get('beige')
        colourRed = request.form.get('red')
        colourOther = request.form.get('other')
        sex = request.form.get('sex')

        
        #prepare data for sql query

        data = {
                "reportType": "Found",
                "petType": petType,
                "postcodeArea": postcodeArea,
                #"sex": sex,
                "black": colourBlack,
                "white": colourWhite,
                "brown": colourBrown,
                "lightBrown": colourLightBrown,
                "grey": colourGrey,
                "beige": colourBeige,
                "red": colourRed,
                "other": colourOther
                }       
        
        
        query, bind_params = j.prepare_query(template, data)
        
        #self.assertEquals(bind_params, [reportType, petType, postcodeArea, sex, colourBlack, colourWhite, colourBrown, colourLightBrown, colourGrey, colourBeige,colourRed, colourOther])
        
        #self.assertEquals(query.strip(), expected_query.strip())
        
        db = get_db()
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        pets = cursor.execute(query, (bind_params)).fetchall()
        
    else:"""
    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    reportType = "Found"
    pets = cursor.execute("SELECT * FROM pet WHERE reportType=?", (reportType,)).fetchall()

    return render_template('pagePets.html', pets=pets, reportType=reportType),200

@app.route('/missing/<petId>/<petName>', methods=('GET', 'POST'))
def missingPet(petId,petName):

    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()

    #pet = cursor.execute("SELECT * FROM pet WHERE petId=?", (petId,)).fetchone()
    pet = cursor.execute("SELECT * FROM pet WHERE petId =?", (petId,)).fetchone()
    
    """if request.method == "POST":
        name = request.form['username']
        comment = request.form['comment']

        cursor.execute("INSERT INTO comments (name, petId, content) VALUES (?,?,?)", (name, petId, comment))

        db.commit()

    comments = cursor.execute("SELECT * FROM comments WHERE petId=?", (petId,)).fetchall()     
    """
    
    petType = cursor.execute("SELECT petType FROM pet WHERE petId=?", (petId,)).fetchone()

    #page = []
    #page.append('<html><p>')
    #page.append(str(pet))
    #page.append('</p></html>')
    #return ''.join(page)

    reportType = "Missing"
    return render_template('comments.html', pet=pet, reportType=reportType, petType=petType),200

@app.route('/found/<petId>', methods=('GET', 'POST'))
def foundPet(petId):
    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()

    #pet = cursor.execute("SELECT * FROM pet WHERE petId=?", (petId,)).fetchone()
    pet = cursor.execute("SELECT * FROM pet WHERE petId =?", (petId,)).fetchone()

    """if request.method == "POST":
        name = request.form['username']
        comment = request.form['comment']

        cursor.execute("INSERT INTO comments (name, petId, content) VALUES (?,?,?)", (name, petId, comment))

        db.commit()

    comments = cursor.execute("SELECT * FROM comments WHERE petId=?", (petId,)).fetchall()
    """
    
    petType = cursor.execute("SELECT petType FROM pet WHERE petId=?", (petId,)).fetchone()

    #page = []
    #page.append('<html><p>')
    #page.append(str(pet))
    #page.append('</p></html>')
    #return ''.join(page)

    reportType = "Found"
    return render_template('comments.html', pet=pet, reportType=reportType, petType=petType),200


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
