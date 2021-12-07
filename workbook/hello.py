from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():



    return """
       <html>
       <head>
         <link rel="stylesheet" type="text/css" href="http://webtech-48.napier.ac.uk/style.css"></head>
       <body>
       <h1>Heading</h1>
       <p>Test Test Test</p>
    <img src="https://images2.minutemediacdn.com/image/upload/c_crop,h_2128,w_3155,x_0,y_534/v1554928552/shape/mentalfloss/540093-istock-514343279.jpg?itok=bMyDmYZ2" width=300px" height="150">
       </body></html>"""
