import unittest
import subprocess
import json
import time
import requests

class TestUserRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask backend in a separate process
        cls.flask_process = subprocess.Popen(['python', '../backend.py'])

        # Give some time for the Flask app to start (you may need to adjust the sleep time)
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        # Terminate the Flask backend process when tests are finished
        cls.flask_process.terminate()
        cls.flask_process.wait()

    def test_create_user(self):
        # Test creating a new user
        data = {
            'name': 'newuser',
            'password': 'password123',
            'role': '5',
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://localhost:5000/createUser', json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        # Test creating a user with missing data
        data = {
            'name': 'newuser',
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://localhost:5000/createUser', json=data, headers=headers)

        self.assertEqual(response.status_code, 500)

    def test_update_user(self):
        # Test creating a new user
        dataCreate = {
            'name': 'newuser',
            'password': 'password123',
            'role': '5',
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://localhost:5000/createUser', json=dataCreate, headers=headers)

        self.assertEqual(response.status_code, 201)

        # Test updating a user
        data = {
            'name': 'newuser',
            'password': 'updatedpassword',
            'role': '0',  # Update the role
        }

        headers = {'Content-Type': 'application/json'}
        user_name = "newuser"  # Replace with the actual user ID you want to update
        response = requests.put(f'http://localhost:5000/updateUser/{user_name}', json=data, headers=headers)

        self.assertEqual(response.status_code, 200)  # 200 for a successful update

        response = requests.delete('http://localhost:5000/deleteUser/newuser')

        self.assertEqual(response.status_code, 204)  # Use 204 for a successful delete

    def test_delete_user(self):
        # Test deleting a user
        response = requests.delete('http://localhost:5000/deleteUser/newuser')

        self.assertEqual(response.status_code, 204)  # Use 204 for a successful delete

    def test_get_user(self):
        # Test getting a user
        response = requests.get('http://localhost:5000/getUser/1')

        self.assertEqual(response.status_code, 200)  # Use 200 for a successful get

if __name__ == '__main__':
    unittest.main()
