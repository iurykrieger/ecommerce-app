from requests import post
from flask import current_app

def create_transaction(cart, payType, address, user):
    return post("http://transaction:3000/transactions", json={
        "cart": cart,
        "payType": payType,
        "address": address,
        "user": user
    }).json()
