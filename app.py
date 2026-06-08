from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "nike_store_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ==========================
# DATABASE MODELS
# ==========================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )


class Product(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    image = db.Column(
        db.String(500),
        nullable=False
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():
    products = Product.query.all()
    return render_template(
        "index.html",
        products=products
    )


# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully")

        return redirect(url_for("login"))

    return render_template("register.html")


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            login_user(user)

            return redirect(url_for("home"))

        flash("Invalid username or password")

    return render_template("login.html")


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("home"))


# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route("/admin")
@login_required
def admin():

    products = Product.query.all()

    return render_template(
        "admin.html",
        products=products
    )
@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    total = sum(
        item["price"]
        for item in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )
@app.route("/remove-from-cart/<int:index>")
def remove_from_cart(index):

    cart = session.get("cart", [])

    if 0 <= index < len(cart):
        cart.pop(index)

    session["cart"] = cart

@app.route("/add-to-cart/<int:product_id>",
    methods=["GET", "POST"])
@login_required
def add_to_cart(product_id):

    if request.method == "POST":

        name = request.form["name"]

        price = float(
            request.form["price"]
        )

        image = request.form["image"]

        product = Product(
            name=name,
            price=price,
            image=image
        )

        db.session.add(product)
        db.session.commit()

        flash("Product Added")

        return redirect(
            url_for("admin")
        )

    return render_template(
        "add_product.html"
    )


# ==========================
# INITIAL PRODUCTS
# ==========================

def create_default_products():

    if Product.query.count() == 0:

        
        products = [

    Product(name="Adidas Black White", price=150, image="images/adidas_black_white.png"),
    Product(name="Air Jordan 1 Retro", price=220, image="images/air_jordan_1_retro.png"),
    Product(name="Air Jordan 11", price=300, image="images/air_jordan_11.png"),
    Product(name="Jordan Blue Neon", price=250, image="images/jordan_blue_neon.png"),
    Product(name="Jordan High Yellow", price=240, image="images/jordan_high_yellow.png"),
    Product(name="Jordan Low Pink", price=230, image="images/jordan_low_pink.png"),
    Product(name="Nike Air Force White", price=190, image="images/nike_air_force_white.png"),
    Product(name="Nike Air Max Grey", price=180, image="images/nike_air_max_grey.png"),
    Product(name="Nike Air Red", price=175, image="images/nike_air_red.png"),

    Product(name="Nike High Top White", price=200, image="images/nike_high_top_white.png"),
    Product(name="Nike Minimal White", price=160, image="images/nike_minimal_white.png"),
    Product(name="Nike Teal Running", price=170, image="images/nike_teal_running.png"),
    Product(name="Nike White Red", price=180, image="images/nike_white_red.png"),
    Product(name="Nike Yellow Silk", price=185, image="images/nike_yellow_silk.png"),
    Product(name="Nike Zoom White", price=210, image="images/nike_zoom_white.png"),

    Product(name="Running Shoe Ground", price=155, image="images/runnin_shoe_ground.png"),
    Product(name="Sneaker Aesthetic", price=195, image="images/sneaker_aesthetic.png"),
    Product(name="Sneaker Feet Socks", price=145, image="images/sneaker_feet_socks.png"),
    Product(name="Sneaker Yellow Black", price=225, image="images/sneaker_yellow_black.png"),
    Product(name="Store Display Neon", price=205, image="images/store_display_neon.png"),
    Product(name="Vans Old Skool Yellow", price=140, image="images/vans_old_skool_yellow.png")

]

            

  
       


            

            
           
             
            

        

        db.session.add_all(products)
        db.session.commit()


# ==========================
# START APP
# ==========================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        create_default_products()

    app.run(
        debug=True
    )
