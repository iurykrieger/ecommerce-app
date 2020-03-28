from flask import current_app
from products import get_product
from functools import reduce
from uuid import uuid4

def get_cart_item_summary (item):
    product = get_product(item.get("id"))
    total = float(product["price"]) * item["quantity"]
    return {
        "id": item.get("id"),
        "quantity": item.get("quantity"),
        "price": float(product.get("price", 0)),
        "name": product.get("name"),
        "image": product.get("images").get("default"),
        "total": total
    }

def build_cart_summary(cart):
    cart["items"] = list(map(lambda item: get_cart_item_summary(item), cart["items"]))
    cart["total"] = reduce(lambda total, item: total + item.get("total", 0), cart["items"], 0)
    return cart

def get_cart(cart_id):
    return current_app.mongo.db.carts.find_one({ "id": cart_id }) or generate_cart()

def generate_cart():
    cart = { "id": str(uuid4()), "items": [] }
    current_app.mongo.db.carts.insert_one(cart)
    return cart

def update_cart_product(cart_id, product_id, quantity = 1):
    cart = get_cart(cart_id)

    cart_items = cart["items"]
    try:
        item = next((item for item in cart_items if item.get("id") == product_id))
        item["quantity"] = quantity
    except StopIteration:
        cart_items.append({
            "id": product_id,
            "quantity": quantity
        })

    current_app.mongo.db.carts.update_one({
        "id": cart.get("id")
    }, {
        "$set": {
            "items": cart_items
        }
    })

    return cart
