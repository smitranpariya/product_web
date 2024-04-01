from flask import Flask, render_template, request, redirect, url_for, flash,session,send_file
from bson import ObjectId
import base64
import bcrypt
from flask_pymongo import PyMongo 
from gridfs import GridFS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

app.config["MONGO_URI"] = "mongodb://localhost:27017/product_web"
mongo = PyMongo(app) 
db = mongo.db
fs = GridFS(db)

@app.route("/", methods=["POST", "GET"])
def login_page():
    return render_template("login_page.html")

@app.route('/dologin', methods=["POST", "GET"])
def dologin():
    if "email" in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        email_check = db.credentials.find_one({"email": email})
        
        if email_check:
            email_val = email_check['email']
            password_check = email_check['password']
            
            # Check if the entered password matches the hashed password in the database
            if bcrypt.checkpw(password.encode('utf-8'),password_check):
                session['email'] = email_val
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password!')
                return render_template('login_page.html')
        else:
            flash("Email not found")
            return redirect(url_for('login_page'))
    return render_template('login_page.html')
    # Modify this to redirect to your login page

@app.route("/signup", methods=["POST", "GET"])
def signup_page():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        email_found = db.credentials.find_one({"email": email})
        user_found = db.credentials.find_one({"username": username})
        if user_found:
            flash("Username already exists")
            return redirect(url_for("signup_page"))  # Redirect to signup page upon username conflict
        if email_found:
            flash("Email already exists")
            return redirect(url_for("signup_page"))  # Redirect to signup page upon email conflict
        if email and username and password:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            db.credentials.insert_one({"email": email, "password": hashed, "username": username})
            return redirect(url_for("dologin"))  # Redirect to the login page after successful signup
    return render_template("signup_page.html")

@app.route('/logout')
def logout():
	session.pop('email',None)
	return redirect('/')

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    if 'email' in session:
        return render_template("main_layout.html")
    else:
        return redirect(url_for('dologin'))
    

@app.route('/products',methods=['POST'])
def products():
    if 'email' in session:
        product_title = request.form.get('product_title')
        product_description = request.form.get('product_description')
        price = request.form.get('price')
        photo = request.files['photo']

        if product_title and product_description and photo:
            file_data = photo.read()
            photo_id = fs.put(file_data, filename=photo.filename)
            form_input = {
            "product_title": product_title,
            "product_description": product_description,
            "price": price,
            "photo": photo_id
            }
            db.products.insert_one(form_input)

        return render_template('products.html')
    else:
        return redirect(url_for('dologin'))
    
@app.route('/products',methods=['GET'])
def products_view():
    if 'email' in session:
        products = db.products.find() 
        products_with_photos = []
        for product in products:
            photo_id = product.get('photo', None)
            if photo_id:
                photo_data = fs.get(ObjectId(photo_id)).read()
                base64_photo_data = base64.b64encode(photo_data).decode('utf-8')
                product['photo_data'] = base64_photo_data
            products_with_photos.append(product) # Corrected from 'product' to 'products'
        return render_template('products.html', products=products_with_photos)  # Corrected variable name to 'products'
    else:
        return redirect(url_for('dologin'))


@app.route('/photo/<photo_id>',methods=['GET'])
def photo(photo_id):
    photo = fs.get(photo_id)
    return send_file(photo,mimetype='image/jpeg')
    
        
    


if __name__ == "__main__":
    app.run(debug=True)
