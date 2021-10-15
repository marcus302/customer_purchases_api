import requests

params = {"customer_id": 1, "product_id": 1, "quantity": 20}

# Delete a customer purchase.
r = requests.delete("http://127.0.0.1:5000/customer_purchase/", params=params)
print(r.status_code, r.content)

# Update a customer purchase.
r = requests.post("http://127.0.0.1:5000/customer_purchase/", params=params)
print(r.status_code, r.content)

params = {"customer_id": 2, "product_id": 1, "quantity": 100}

# Create a new customer purchase.
r = requests.post("http://127.0.0.1:5000/customer_purchase/", params=params)
print(r.status_code, r.content)

# List customer purchases.
r = requests.get("http://127.0.0.1:5000/customer/2")
print(r.status_code, r.content)
