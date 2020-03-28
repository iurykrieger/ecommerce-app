from flask import current_app
from functools import reduce
from datetime import date
from uuid import uuid4

def create_transaction(cart, payType, address, user):
    transaction = {
        "id": str(uuid4()),
        "cart": cart,
        "payType": payType,
        "address": address,
        "user": user,
        "total": cart.get("total", 0),
        "date": str(date.today()),
        "status": False
    }
    current_app.mongo.db.transactions.insert_one(transaction)
    return transaction

def validate_transaction(transaction):
    transaction["status"] = True
    return transaction