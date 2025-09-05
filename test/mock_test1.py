import requests, unittest
from unittest.mock import Mock,patch

def get_code(url):
    response=requests.get(url)
    return response.status_code

class Testcode (unittest.TestCase):

    @patch('requests.get')
    def test_code(self,mock_url):
        mock_resp=Mock()
        mock_resp.status_code=200
        mock_url.return_value=mock_resp

        user_code= get_code("https://api.com")
        mock_url.assert_called_once_with("https://api.com")
        self.assertEqual(user_code,200)

if __name__=="__main__":
    unittest.main()
