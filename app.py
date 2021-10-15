from flask import Flask

app = Flask(__name__)


@app.route("/customer_purchase/<customer_purchase_id>", methods=["POST", "DELETE"])
def customer_purchase(customer_purchase_id):
    return f"<p>Hello, {customer_purchase_id}!</p>"


@app.route("/customer/<customer_id>", methods=["GET"])
def customer(customer_id):
    return f"<p>Hello, {customer_id}!</p>"