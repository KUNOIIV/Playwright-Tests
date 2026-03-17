import requests
import pytest 

# Full API suite: tests endpoints (GET/POST/DELETE), asserts status codes + JSON data

BASE_URL = "https://jsonplaceholder.typicode.com/"  

def test_get_users(): #Test GET: fetch lists of users
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200 #The server should say OK good
    assert len(response.json()) == 10  # it returns 10 fake users
    print("Users fetched:", len(response.json()))

def test_create_post(): #Test POST: create a new post
    payload = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()

def test_delete_post(): #Test DELETE: Removing a post
    create_payload = {"title": "Delete me", "body": "Temp post", "userId": 1}
    create_response = requests.post(BASE_URL + "posts", json=create_payload)
    post_id = create_response.json() # Grab the fake ID it gave

    # Now it will delete it
    delete_response = requests.delete(BASE_URL + f"posts/{post_id}")
    assert delete_response.status_code == 200  # jsonplaceholder returns 200 on delete (even though fake)
    print(f"Deleted post ID {post_id} successfully")

    get_after_delete = requests.get(BASE_URL + f"posts/{post_id}")
    assert get_after_delete.status_code == 404  
    print("Post is gone:", get_after_delete.status_code)
