from django.test import TestCase

# Create your tests here.
import requests

BASE_URL = "http://127.0.0.1:8000/rello/api/v1/"
TEST_RESULTS_FILE = "test_results.txt"

def write_result(endpoint_name, method, headers, body, response):
    with open(TEST_RESULTS_FILE, 'a') as file:
        file.write(f"Endpoint: {endpoint_name}\n")
        file.write(f"Method: {method}\n")
        file.write(f"Request Headers: {headers}\n")
        if body:
            file.write(f"Request Body: {body}\n")
        file.write(f"Response: {response}\n")
        for(key, value) in response.headers.items():
            file.write(f"Response Header: {key}: {value}\n")
        file.write("\n")

def test_get_boards():
    endpoint_name = "List all boards"
    url = f"{BASE_URL}boards/"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    write_result(endpoint_name, "GET", headers, None, response)

def test_create_board():
    endpoint_name = "Create a new board"
    url = f"{BASE_URL}boards/"
    headers = {"Content-Type": "application/json"}
    body = {"name": "Test Board", "description": "A board for testing"}
    response = requests.post(url, headers=headers,json=body)
    write_result(endpoint_name, "POST", headers, body, response)

def test_get_board(board_id):
    endpoint_name = f"Retrieve a specific board"
    url = f"{BASE_URL}boards/{board_id}/"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    write_result(endpoint_name, "GET", headers, None, response)

def test_update_board(board_id):
    endpoint_name = "Update a specific board"
    url = f"{BASE_URL}boards/{board_id}/"
    headers = {"Content-Type": "application/json"}
    body = {"name": "Updated Test Board", "description": "Updated description"}
    response = requests.put(url, headers=headers, json=body)
    write_result(endpoint_name, "PUT", headers, body, response)

def test_delete_board(board_id):
    endpoint_name = "Delete a specific board"
    url = f"{BASE_URL}boards/{board_id}/"
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    write_result(endpoint_name, "DELETE", headers, None, response)

#test all functions and write
test_get_boards()
test_create_board()