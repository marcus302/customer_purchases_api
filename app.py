from flask import Flask, jsonify, request
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
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"),
                            nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"),
                           nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    # TODO: Make sure customer purchases are deleted in cascade when a customer or product is removed.
    customer = db.relationship("Customer", backref=db.backref("customer_purchases"))
    product = db.relationship("Product", backref=db.backref("customer_purchases"))

    def __repr__(self):
        return f"{self.quantity} pieces of {self.product_id} for {self.customer_id}"
    
    # TODO: If I had the time to implement Marshmallow, this would be unnecessary.
    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.name


db.create_all()
Customer.query.delete()
Product.query.delete()
CustomerPurchase.query.delete()
db.session.commit()
c = Customer(first_name="Mark", last_name="de Wijk", address="Bloemsingel 157")
p = Product(name="Ferrari")
cp = CustomerPurchase(quantity=5, customer=c, product=p)
db.session.add(c)
db.session.add(p)
db.session.add(cp)
db.session.commit()


@app.route("/customer_purchase/", methods=["POST", "DELETE"])
def customer_purchase():
    customer_id = request.args.get("customer_id")
    product_id = request.args.get("product_id")
    if request.method == "DELETE":
        customer_purchase = CustomerPurchase.query.filter_by(
            customer_id=customer_id,
            product_id=product_id
        ).one()
        db.session.delete(customer_purchase)
        db.session.commit()
        return jsonify({"success": True}), 200
    elif request.method == "POST":
        quantity = request.args.get("quantity")
        customer_purchase = CustomerPurchase.query.filter_by(
            customer_id=customer_id,
            product_id=product_id
        ).first()
        if customer_purchase is not None:
            # Combination already exists, so update.
            customer_purchase.quantity = quantity
            db.session.add(customer_purchase)
            db.session.commit()
            return jsonify({"success": True}), 200
        else:
            # Combination does not yet exist, so add it.
            customer = Customer.query.filter_by(id=customer_id).one()
            product = Product.query.filter_by(id=product_id).one()
            customer_purchase = CustomerPurchase(quantity=quantity, customer=customer, product=product)
            db.session.add(customer_purchase)
            db.session.commit()
            return jsonify({"success": True}), 200


@app.route("/customer/<customer_id>", methods=["GET"])
def customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).one()
    return jsonify(json_list=[x.to_json() for x in customer.customer_purchases])
