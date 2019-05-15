import unittest
import sys
import os

sys.path.append("..")
from PastaOndeOLuisFazTestes.DbCommunicator import DbCommunicator

class TestDb(unittest.TestCase):

    def test_add(self):
      for filename in os.listdir("./images_to_populate_db"):
        
        result =DbCommunicator.add(open('./images_to_populate_db/' + filename, 'rb').read())
        self.assertIs(result,'./images_to_populate_initial_db/' + filename)
if __name__ == '__main__':
        unittest.main()





        