from requests import get, post

def get_products(page=1, per_page=24):
    products = get("http://catalog:3000/products/list", params={ "page": page, "pageSize": per_page }).json()
    return products["rows"]

def get_product(product_id):
    return get("http://catalog:3000/products/get", params={ "id": product_id }).json()