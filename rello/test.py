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
        file.write(f"Response: {response.json()}\n")
        file.write(f"Status Code: {response.status_code}\n")
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
    response = requests.post(url, headers=headers, json=body)
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

def test_create_list(board_id):
    endpoint_name = "Create a new list"
    url = f"{BASE_URL}lists/"
    headers = {"Content-Type": "application/json"}
    body = {"name": "Test List", "board": board_id, "position": 1}
    response = requests.post(url, headers=headers, json=body)
    write_result(endpoint_name, "POST", headers, body, response)
    return response.json()['id']

def test_get_list(list_id):
    endpoint_name = f"Retrieve a specific list"
    url = f"{BASE_URL}lists/{list_id}/"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    write_result(endpoint_name, "GET", headers, None, response)

def test_update_list(list_id):
    endpoint_name = "Update a specific list"
    url = f"{BASE_URL}lists/{list_id}/"
    headers = {"Content-Type": "application/json"}
    body = {"name": "Updated Test List", "position": 1}
    response = requests.put(url, headers=headers, json=body)
    write_result(endpoint_name, "PUT", headers, body, response)

def test_delete_list(list_id):
    endpoint_name = "Delete a specific list"
    url = f"{BASE_URL}lists/{list_id}/"
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    write_result(endpoint_name, "DELETE", headers, None, response)

def test_change_list_position(board_id, list_id, new_position):
    endpoint_name = "Change list position"
    url = f"{BASE_URL}boards/{board_id}/lists/{list_id}/position/"
    headers = {"Content-Type": "application/json"}
    body = {"position": new_position}
    response = requests.put(url, headers=headers, json=body)
    write_result(endpoint_name, "PUT", headers, body, response)

def main():
    # Clear previous results
    with open(TEST_RESULTS_FILE, 'w') as file:
        file.write("")

    # Test board endpoints
    test_get_boards()
    board_id = test_create_board()
    test_get_board(board_id)
    test_update_board(board_id)
    test_delete_board(board_id)

    # Test list endpoints
    test_get_boards()
    board_id = test_create_board()
    list_id = test_create_list(board_id)
    test_get_list(list_id)
    test_update_list(list_id)
    test_delete_list(list_id)

    # Test changing list position
    test_get_boards()
    board_id = test_create_board()
    list_id1 = test_create_list(board_id)
    list_id2 = test_create_list(board_id)
    test_change_list_position(board_id, list_id1, 2)
    test_change_list_position(board_id, list_id2, 1)

if __name__ == "__main__":
    main()
