from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def login():
    return "hello world"

app.run(debug=True)