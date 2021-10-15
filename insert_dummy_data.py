from app import db
from models import Customer, Product, CustomerPurchase

db.create_all()
# Clear tables.
Customer.query.delete()
Product.query.delete()
CustomerPurchase.query.delete()
db.session.commit()
# Create some dummy data.
mark = Customer(first_name="Mark", last_name="de Wijk", address="Bloemsingel 157")
jamal = Customer(first_name="Jamal", last_name="Bakker", address="Kardinge 2")
maarten = Customer(first_name="Maarten", last_name="de Boer", address="Ebbingestraat 3")
ferrari = Product(name="Ferrari")
lambo = Product(name="Lamborghini")
cp1 = CustomerPurchase(quantity=5, customer=mark, product=ferrari)
cp2 = CustomerPurchase(quantity=1, customer=maarten, product=lambo)
for x in [mark, jamal, maarten, ferrari, lambo, cp1, cp2]:
    db.session.add(x)
db.session.commit()
