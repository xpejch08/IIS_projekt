import unittest
import subprocess
import json
import time
import requests

class TestAppRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask backend in a separate process
        cls.flask_process = subprocess.Popen(['python', '../backend.py'])
        # Define the base URL variable
        cls.BASE_URL = 'http://localhost:5000/'
        # Give some time for the Flask app to start
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        # Terminate the Flask backend process when tests are finished
        cls.flask_process.terminate()
        cls.flask_process.wait()

    # ... Existing User tests ...

    def test_add_subject(self):
        # Test adding a new subject with lowercase keys
        data = {
            'shortcut': 'BIO101',
            'name': 'Biology 101',
            'annotation': 'Introduction to Biology',
            'credits': 4,
            'id_guarantor': 2  # Assuming there's a guarantor with ID 2
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{self.BASE_URL}/addSubject', json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

    def test_delete_subject(self):
        # First, add a subject to delete
        add_data = {
            'shortcut': 'PHY102',
            'name': 'Physics 102',
            'annotation': 'Advanced Physics',
            'credits': 5,
            'id_guarantor': 2
        }
        add_headers = {'Content-Type': 'application/json'}
        add_response = requests.post(f'{self.BASE_URL}/addSubject', json=add_data, headers=add_headers)
        subject_id = add_response.json().get('id')

        # Test deleting the subject
        delete_response = requests.delete(f'{self.BASE_URL}/deleteSubject/{subject_id}')

        self.assertEqual(delete_response.status_code, 204)
        delete_response = requests.delete(f'{self.BASE_URL}/deleteSubject/4')

    def test_get_subject(self):
        # First, add a subject to get
        add_data = {
            'shortcut': 'CHEM102',
            'name': 'Chemistry 102',
            'annotation': 'Advanced Chemistry',
            'credits': 5,
            'id_guarantor': 2
        }
        add_headers = {'Content-Type': 'application/json'}
        add_response = requests.post(f'{self.BASE_URL}/addSubject', json=add_data, headers=add_headers)

        # Ensure the subject was added successfully before proceeding
        self.assertEqual(add_response.status_code, 201)

        subject_id = add_response.json().get('id')
        self.assertIsNotNone(subject_id, "Failed to add subject and get its ID")

        # Test getting the subject
        get_response = requests.get(f'{self.BASE_URL}/getSubject/{subject_id}')

        self.assertEqual(get_response.status_code, 200)

        # Assuming the 'as_dict' method returns attributes in lowercase
        self.assertEqual(get_response.json().get('name'), add_data['name'])
        delete_response = requests.delete(f'{self.BASE_URL}/deleteSubject/6')


    def test_set_guarantor_of_subject(self):
        # Ensure a subject and a user (new guarantor) exist
        # You might want to add a user and a subject here if they do not exist already
        # For demonstration, let's assume the user and subject already exist

        # Data to change the guarantor of the subject
        data = {
            'shortcut': 'matala',  # Assuming this subject already exists
            'guarantor_name': 'garant'  # Assuming this user already exists
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.put(f'{self.BASE_URL}/setGuarantorOfSubject', json=data, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_add_teaching_activity(self):
        # Data for creating a new teaching activity
        data = {
            'label': 'Intro to Programming',
            'duration': 60,
            'repetition': 'weekly',
            'subject_shortcut': 'matala'  # Assuming this subject already exists
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{self.BASE_URL}/addTeachingActivity', json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

    def test_delete_teaching_activity(self):
        # First, create a teaching activity to delete
        add_data = {
            'label': 'Test Activity',
            'duration': 45,
            'repetition': 'weekly',
            'subject_shortcut': 'matala'  # Assuming this subject already exists
        }
        add_headers = {'Content-Type': 'application/json'}
        add_response = requests.post(f'{self.BASE_URL}/addTeachingActivity', json=add_data, headers=add_headers)

        # Ensure the teaching activity was added successfully before proceeding
        self.assertEqual(add_response.status_code, 201)

        # Test deleting the teaching activity
        delete_response = requests.delete(f'{self.BASE_URL}/deleteTeachingActivity/{add_data["label"]}')
        self.assertEqual(delete_response.status_code, 200)

        # Optionally, verify that the teaching activity no longer exists in the database
        # This would require a GET request or similar to check for its existence


if __name__ == '__main__':
    unittest.main()
