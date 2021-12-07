from flask import Flask, request, url_for
app = Flask(__name__)

@app.route("/")
def root():
    return "The default, 'root' route"

@app.route("/display")
def display():
    return '<img src="'+url_for('static', filename='uploads/file.png')+'"/>'

@app.route("/upload/", methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        f = request.files['datafile']
        f.save('static/img/paw.svg')
        return "File Uploaded"
    else:
        page ='''
        <html><body>
            <form action="" method="post" name="form" enctype="multipart/form-data">
                <input type="file" name="datafile"/>
                <input type="submit" name="submit" id="submit"/>
            </form>
        </body></html>'''
        return page, 200

@app.route("/hello")
def hello():
    name = request.args.get('name', '')
    if name == '':
        return "no params supplied"
    else:
        return "Hello %s" % name

@app.route("/add/<int:first>/<int:second>")
def add(first, second):
    return str(first+second)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
