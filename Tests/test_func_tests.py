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
      assert 'original' in res[1] and 'image' in res[1] and 'box' in res[1] and 'confidence' in res[1] and 'class' in res[1]
      assert isinstance(res[1]['original']  , str)
      assert isinstance(res[1]['image']     , str)
      assert isinstance(res[1]['box']       , dict)
      assert isinstance(res[1]['confidence'], int)
      assert isinstance(res[1]['class']     , str)
  files = {'image': open("./TestImages/Screenshot_2019-06-09-20-28-38.png", 'rb').read()}
    print(r.text)