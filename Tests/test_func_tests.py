import pytest
import random
import os
import requests
import json

NUMTESTS = 10
image_list = []
for filename in os.listdir("./TestImages"):
  image_list.append(open("./TestImages/" + filename, 'rb').read())

def test_put():
  url = 'http://127.0.0.1:10002/put'
  for _ in range(NUMTESTS):
    files = {'image': random.choice(image_list)}
    r = requests.post(url, files=files)
    res = json.loads(r.text)
    if(res[0] == "Image Added Successfully"):
      for i in res[1]:
        assert 'original' in i and 'image' in i and 'box' in i and 'confidence' in i and 'class' in i
        assert isinstance(i['original']  , str)
        assert isinstance(i['image']     , str)
        assert isinstance(i['box']       , dict)
        assert isinstance(i['confidence'], int)
        assert isinstance(i['class']     , str)
  files = {'image': open("./TestImages/Screenshot_2019-06-09-20-28-38.png", 'rb').read()}
  r = requests.post(url, files=files)
  res = json.loads(r.text)
  assert res[0] == "Any class detected"

# todos os outros testes funcionais são analogos aos testes das funções respetivas