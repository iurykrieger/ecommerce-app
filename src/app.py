from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_pymongo import PyMongo
from carts import update_cart_product, get_cart, build_cart_summary
from products import get_products, get_product
from transactions import create_transaction, validate_transaction
from os import environ

app = Flask(__name__)
app.config["MONGO_URI"] = environ.get("MONGO_URI")
app.mongo = PyMongo(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/products/", methods=["GET"])
def products():
    page = int(request.args.get("page", 1))
    next_page = page + 1
    return render_template("products.html", products=get_products(page=page), next_page=next_page)

@app.route("/products/<string:product_id>", methods=["GET"])
def product(product_id):
    db_product = get_product(product_id)
    return render_template("product.html", product=db_product)

@app.route("/cart/", methods=["GET"])
def cart():
    cart = build_cart_summary(get_cart(request.cookies.get("cart_id")))
    
    cart_response = make_response(render_template("cart.html", cart=cart))
    cart_response.set_cookie("cart_id", cart.get("id"))
    
    return cart_response

@app.route("/cart/add/<string:product_id>", methods=["POST"])
def add_cart_product(product_id):
    cart_redirect = make_response(redirect(url_for("cart")))
    cart = update_cart_product(
        cart_id=request.cookies.get("cart_id"),
        product_id=product_id,
        quantity=int(request.form.get("quantity", 1))
    )
    cart_redirect.set_cookie("cart_id", cart.get("id"))
    return cart_redirect

@app.route("/cart/cancel", methods=["POST"])
def close_cart():
    cart_redirect = make_response(redirect(url_for("index")))
    cart_redirect.set_cookie("cart_id", "")
    return cart_redirect

@app.route("/checkout", methods=["GET"])
def checkout():
    cart = build_cart_summary(get_cart(request.cookies.get("cart_id")))
    shipping = 150
    total = cart.get("total") + shipping
    return render_template("checkout.html", cart=cart, shipping=shipping, total=total)

@app.route("/transaction", methods=["POST"])
def transaction():
    transaction = create_transaction(
        cart=get_cart(request.cookies.get("cart_id")),
        payType=request.form.get("payType"),
        address={
            "zipCode": request.form.get("zipCode"),
            "country": request.form.get("country"),
            "city": request.form.get("city")
        },
        user={
            "name": request.form.get("name"),
            "lastname": request.form.get("lastname"),
            "company": request.form.get("company"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email")
        }
    )

    validate_transaction(transaction)
    transaction["cart"] = build_cart_summary(transaction.get("cart"))

    transaction_response = make_response(render_template("confirmation.html", transaction=transaction))
    transaction_response.set_cookie("cart_id", "")

    return transaction_response