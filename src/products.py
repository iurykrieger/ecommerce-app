from flask import current_app

def get_products(page=1, per_page=24):
    return current_app.mongo.db.products.find({}).skip(per_page * page).limit(per_page)

def get_product(product_id):
    return current_app.mongo.db.products.find_one_or_404({ "id": product_id })