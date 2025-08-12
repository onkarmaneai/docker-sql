import requests
import time

BASE = "http://localhost:8000"

# initialize DB/table
print(requests.post(f"{BASE}/init").json())
# add a row
r = requests.post(f"{BASE}/add", json={"name": "alpha", "value": 100})
print("added:", r.json())
item_id = r.json()["id"]

# list rows
print("all:", requests.get(f"{BASE}/items").json())

# fetch one
print("fetch:", requests.get(f"{BASE}/item/{item_id}").json())