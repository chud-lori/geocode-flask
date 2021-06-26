from setup import app
import unittest

class GeoTestCase(unittest.TestCase):
    def __init__(self) -> None:
        tester = app.test_client(self)
    #check for response 200
    def test_index(self):
        response = self.tester.get('/')
        statuscode = response.status_code
        self.assertEquals(statuscode, 200)
    
    def test_invalid_location(self):
        location = 'wro93729s' # random string
        response = self.tester.get('/?',location)
        statuscode = response.status_code
        self.assertEquals(statuscode, 404)

if __name__ == "__main__":
    unittest.main()