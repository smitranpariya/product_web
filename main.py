from flask import Flask, render_template, request, redirect, url_for, flash,session
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
    return render_template("main_layout.html")
    


if __name__ == "__main__":
    app.run(debug=True)
