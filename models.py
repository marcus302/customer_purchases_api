from app import db

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
