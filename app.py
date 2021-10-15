from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    # TODO: Split into street name, house number, city, postal code and country?
    address = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class CustomerPurchase(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.quantity} pieces of {self.product_id} for {self.customer_id}"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.name


@app.route("/customer_purchase/<customer_purchase_id>", methods=["POST", "DELETE"])
def customer_purchase(customer_purchase_id):
    return f"<p>Hello, {customer_purchase_id}!</p>"


@app.route("/customer/<customer_id>", methods=["GET"])
def customer(customer_id):
    return f"<p>Hello, {customer_id}!</p>"
