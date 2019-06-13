import pytest
import random
import os
import requests
import json
from hashlib import md5
import sqlite3
NUMTESTS = 10
image_list = []
for filename in os.listdir("./TestImages"):
  image_list.append(open("./TestImages/" + filename, 'rb').read())

#Como a funcionalidade dos metodos relativos ao requests já é testada nos testes unitarios
# aqui apenas vão ser testadas as mensagens de erro
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


def test_get():
  r = requests.get('http://127.0.0.1:10002/get?id=' + md5(bytes(random.randint(0,10))).hexdigest())
  assert r.json() == "Image Not Found"

def test_list():
  request_list = [
    "http://127.0.0.1:10002/list?type=name",
    "http://127.0.0.1:10002/list?type=detect",
    "http://127.0.0.1:10002/list?type=detect&thr=1",
    "http://127.0.0.1:10002/list?type=detect&name=asd",
    "http://127.0.0.1:10002/list?type=detect&name=asd&thr=2",
    "http://127.0.0.1:10002/list?type=detect&name=as",
    "http://127.0.0.1:10002/list?type=detect&name=as123123",
    "http://127.0.0.1:10002/list?type=detect&name=asasdss&page=1",
    "http://127.0.0.1:10002/list?type=detect&name=asasdss&page=1&per_page=32",
  ]
  for _ in range(NUMTESTS):
    request = random.choice(request_list)
    r = requests.get(request)
    assert r.json() == "Bad Call"


def test_garbage_collect():
  for filename in os.listdir("./../BackEnd/images"):
    os.remove('./../BackEnd/images/'+filename)
    db = sqlite3.connect("./../BackEnd/app_db.db")
    db.execute('delete from RelImgCaract')
    db.execute('delete from Imagens')
    db.commit()
    db.close()