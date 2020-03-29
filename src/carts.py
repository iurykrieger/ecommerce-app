from requests import get, post

def build_cart_summary(cart):
    return get("http://cart:3000/carts/getSummary", params={ "id": cart.get("id") }).json()

def get_cart(cart_id):
    return get("http://cart:3000/carts/getOrGenerate", params={ "id": cart_id }).json()

def update_cart_product(cart_id, product_id, quantity = 1):
    return get("http://cart:3000/carts/addProduct", params={ "id": cart_id, "productId": product_id, "quantity": quantity }).json()
