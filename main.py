from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo 
from gridfs import GridFS
from io import BytesIO

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/product_web"
mongo = PyMongo(app) 
db = mongo.db
fs = GridFS(db)

@app.route("/", methods=["GET"])
def login_page():
    return render_template("login_page.html")

@app.route("/do_login", methods=["POST"])
def do_login():
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password:
        db.admin.insert_one({"email": email, "password": password})
        return 'Form submitted successfully. Password: {}, Email: {}'.format(password, email)
    else:
        return 'Error: Empty email or password.'

@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup_page.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("main_layout.html")

@app.route("/products", methods=["POST","GET"])
def add_product():
    product_title = request.form.get("product_title")
    product_description = request.form.get("product_description")
    price = request.form.get("price")
    photo = request.files.get("photo")
    print(photo)
    if product_title and price and photo:
        file_data = photo.read()
        photo_id = fs.put(file_data, filename=photo.filename)
        form_input = {
            "product_title": product_title,
            "product_description": product_description,
            "price": price,
            "photo": photo_id
        }
        db.products.insert_one(form_input)
        return redirect(url_for('dashboard'))
    return render_template("products.html")

if __name__ == "__main__":
    app.run(debug=True)
