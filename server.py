from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/challenge')
def challenge():
    return render_template('challenge.html')

if __name__ == '__main__':
   app.run(debug = True, port=5001)