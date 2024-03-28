from flask import Flask,render_template,request
from flask_pymongo import PyMongo 

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/product_web"
mongo = PyMongo(app) 
db = mongo.db



@app.route("/",methods=["POST" , "GET"])
def login():
        return render_template("login_page.html")

@app.route("/do_login",methods=["POST","GET"])
def do_login():
        
        email = request.form.get("email")
        password = request.form.get("password")

        form_input = {"email":email,
                      "password":password}
        db.admin.insert_one(form_input)
        return  'Form submitted successfully. password: {}, Email: {}'.format(password, email)

@app.route("/signup",methods=["POST","GET"]) 
def signup():
        return render_template("signup_page.html")


app.run(debug=True)