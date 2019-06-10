import pytest
import random
from './../BackEnd/DbCommunicator' import DbCommunicator, hueFromRBG
NUMTESTS = 5

def test_rgb_to_hue():
  for _ in range(NUMTESTS):
    result = hueFromRBG(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    assert(0 < result < 360)
    
def test_add():
  for _ in range(5):
    
