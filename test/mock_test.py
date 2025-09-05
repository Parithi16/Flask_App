import unittest
import requests
from unittest.mock import Mock,patch

def get_user(user_id):
    response=requests.get(f"https://api.example.com/{user_id}")
    return response.json()

class Testmocking(unittest.TestCase):

    @patch('requests.get')
    def test_get(self, mock_get):
        mock_response=Mock()
        resp_dict={"name":"parithi","age":14}
        mock_response.json.return_value=resp_dict
        mock_get.return_value= mock_response

        user_data=get_user(2)
        mock_get.assert_called_with("https://api.example.com/1")
        self.assertEqual(user_data,resp_dict)

if __name__=="__main__":
    unittest.main()


