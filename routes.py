from app import app, db
from flask import jsonify, request
from models import Customer, Product, CustomerPurchase

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
            # Combination already exists, so update it.
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
    return jsonify(json_list=[x.to_json() for x in customer.customer_purchases]), 200
