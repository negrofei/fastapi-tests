import requests

print('Getting items ...')
print(requests.get("http://127.0.0.1:8000/items").json())



### ----------------------------
# ### Esto es con items definido en el archivo
# # Get all items
# print('Getting all items ...')
# print(requests.get("http://127.0.0.1:8000/").json()) 

# # Get item 
# print('Getting item 1 ...')
# print(requests.get("http://127.0.0.1:8000/items/1").json()) 

# # Get item by parameters
# print('Getting item with name=Nails ...')
# print(requests.get("http://127.0.0.1:8000/items?name=Nails").json()) 

# # Adding item
# print("Adding an item:")
# print(
#     requests.post(
#         "http://127.0.0.1:8000/",
#         json={"name": "Screwdriver", "price": 3.99, "quantity": 10, "id": 4, "category": "tools"},
#     ).json()
# )
 

# # Adding item again
# print("Adding same item:")
# print(
#     requests.post(
#         "http://127.0.0.1:8000/",
#         json={"name": "Screwdriver", "price": 3.99, "quantity": 10, "id": 4, "category": "tools"},
#     ).json()
# )

# # Get all items
# print('Getting all items again ...')
# print(requests.get("http://127.0.0.1:8000/").json())

# # Update item 4
# print("Updating item 2 ...")
# print(
#     requests.put(
#         "http://127.0.0.1:8000/items/2?price=0.99"
#     ).json()
# )

# # delete item 4
# print("Deleting item 4 ...")
# print(
#     requests.delete(
#         "http://127.0.0.1:8000/items/4"
#     ).json()
# )