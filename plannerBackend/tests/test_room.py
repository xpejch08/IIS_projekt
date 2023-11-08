import unittest
import subprocess
import time
import requests

class TestRoomRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flask_process = subprocess.Popen(['python', '../backend.py'])
        cls.BASE_URL = 'http://172.18.0.2:5000/'
        #cls.BASE_URL = 'http://localhost:5000/'
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.flask_process.terminate()
        cls.flask_process.wait()

    def test_add_room(self):
        data = {
            'title': 'G106',
            'capacity': 40
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{self.BASE_URL}/createRoom', json=data, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_delete_room(self):
        add_data = {
            'room_number': '102',
            'building': 'Science Hall',
            'capacity': 30
        }
        add_headers = {'Content-Type': 'application/json'}
        add_response = requests.post(f'{self.BASE_URL}/addRoom', json=add_data, headers=add_headers)
        room_id = add_response.json().get('id')
        delete_response = requests.delete(f'{self.BASE_URL}/deleteRoom/{room_id}')
        self.assertEqual(delete_response.status_code, 204)

    def test_update_room(self):
        add_data = {
            'room_number': '103',
            'building': 'Science Hall',
            'capacity': 25
        }
        add_headers = {'Content-Type': 'application/json'}
        add_response = requests.post(f'{self.BASE_URL}/addRoom', json=add_data, headers=add_headers)
        room_id = add_response.json().get('id')

        update_data = {
            'room_number': '103A',
            'building': 'Science Hall Updated',
            'capacity': 50
        }
        update_response = requests.put(f'{self.BASE_URL}/updateRoom/{room_id}', json=update_data, headers=add_headers)
        self.assertEqual(update_response.status_code, 200)

        get_response = requests.get(f'{self.BASE_URL}/getRoom/{room_id}')
        self.assertEqual(get_response.json().get('room_number'), update_data['room_number'])

    def test_get_room(self):
        add_data = {
            'room_number': '104',
            'building': 'Science Hall',
            'capacity': 20
        }
        add_headers = {'Content-Type': 'application/json'}
        add_response = requests.post(f'{self.BASE_URL}/addRoom', json=add_data, headers=add_headers)
        room_id = add_response.json().get('id')

        get_response = requests.get(f'{self.BASE_URL}/getRoom/{room_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get('room_number'), add_data['room_number'])

if __name__ == '__main__':
    unittest.main()
