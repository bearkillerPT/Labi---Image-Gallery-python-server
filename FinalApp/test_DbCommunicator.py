import unittest
from FinalApp import DbCommunicator

class TestDb(unittest.TestCase):

    def test_add(self):
        result = DbCommunicator.add(open('./images_to_populate_initial_db/OOIkfjMdmdQ', 'rb'))
        self.assertIs(result,'./images_to_populate_initial_db/OOIkfjMdmdQ')

if __name__ == '__main__':
        unittest.main()