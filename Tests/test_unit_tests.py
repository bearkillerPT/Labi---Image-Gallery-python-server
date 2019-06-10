import pytest
import random
import os
import os.path
from hashlib import md5
import sys
sys.path.insert(0, './../BackEnd/')
import sqlite3
from DbCommunicator import DbCommunicator, hueFromRBG, __clear_all_caution__
NUMTESTS = 10
image_list = []
for filename in os.listdir("./TestImages"):
  image_list.append(open("./TestImages/" + filename, 'rb').read())
comm = DbCommunicator("test_db.db")

def test_rgb_to_hue():
  for _ in range(NUMTESTS):
    result = hueFromRBG(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    assert(0 < result < 360)

def test_get_dims_and_color():
  for _ in range(NUMTESTS):
    c_image = random.choice(os.listdir("./TestImages"))
    height, width, hue = comm.get_dims_and_color("./TestImages/" + c_image)
    assert height > 0
    assert width > 0
    assert 0 < hue < 360

def test_request_caracteristics():
  for _ in range(NUMTESTS):
    c_image = random.choice(image_list)
    results = comm.request_caracteristics(c_image, "")
    for result in results:
      assert 'name' in result and 'class' in result and 'box' in result and 'confidence' in result
      assert isinstance(result['name'],       str)
      assert isinstance(result['class'],      str)
      assert isinstance(result['box'],        dict)
      assert isinstance(result['confidence'], float)

def test_add():
  __clear_all_caution__('test_db.db')
  for _ in range(NUMTESTS):
    c_image = random.choice(image_list)
    msg = comm.add(c_image)
    if(msg == "Image Added Successfully"): 
      db = sqlite3.connect("test_db.db")
      result = db.execute("select FKOriginalImageName, FKCroppedImageName from RelImgCaract;").fetchall()
      assert len(result) > 0
      for i in result:
        try:
          open("./images/" + i[0])
          open("./images/" + i[1])
          assert True
        except:
          print(i[0],i[1])
          assert False
      db.close()
  assert comm.add(open("./TestImages/Screenshot_2019-06-09-20-28-38.png", 'rb').read()) == "Any class detected"
  __clear_all_caution__('test_db.db')
    
def test_remove():
  __clear_all_caution__('test_db.db')
  for _ in range(NUMTESTS):
    c_image = random.choice(image_list)
    msg = comm.add(c_image)
    db = sqlite3.connect("test_db.db")
    result = db.execute("select FKOriginalImageName, FKCroppedImageName from RelImgCaract;").fetchall()
    if(msg == "Image Added Successfully"): 
      comm.remove({'image_name': md5(c_image).hexdigest()})
    for i in result:
      try:
        open("./images/" + i[0])
        open("./images/" + i[1])
        assert False
      except:
        print(i[0],i[1])
        assert True
    db.close()
  assert(comm.remove(123) == "Bad Call")
  assert(comm.remove({'image': b'ase12312usad79p12e8n9owmed'}) == "Image does not exist in database")
  __clear_all_caution__('test_db.db')

def test_get():
  __clear_all_caution__('test_db.db')
  image_names = []
  for i in image_list:
    result = comm.add(i)
    print(result)
    if(result == "Image Added Successfully"): 
      image_names.append(md5(i).hexdigest())
  for _ in range(NUMTESTS):
    results = comm.get(random.choice(image_names))
    for result in results:
      assert 'original' in result and 'image' in result and 'box' in result and 'confidence' in result and 'class' in result
      assert isinstance(result['original']  , str)
      assert isinstance(result['image']     , str)
      assert isinstance(result['box']       , dict)
      assert isinstance(result['confidence'], int)
      assert isinstance(result['class']     , str)
  __clear_all_caution__('test_db.db')

def test_request():
  __clear_all_caution__('test_db.db')
  for i in image_list:
    comm.add(i)
  r1 = comm.request({'type': 'names'})
  assert isinstance(r1, list) 
  
  r2 = comm.request({'type': 'detected'})
  assert isinstance(r2, list)
  keys = []
  for i in r2:
    keys.append(i['class'])
    assert isinstance(i, dict)

  r3 = comm.request({'type' : 'detected', 'name' : keys[0]})
  print(r3)
  for i in r3[keys[0]]:
    assert 'original' in i and 'image' in i and 'confidence' in i
    assert isinstance(i['original'], str)
    assert isinstance(i['image'], str)
    assert isinstance(i['confidence'], int)
  r4 = comm.request({
    'type' : 'detected', 
    'name' : keys[0], 
    'color': {
      'R':random.randint(0,255),
      'G':random.randint(0,255),
      'B':random.randint(0,255),
      'tol':random.random()
      }
  })
  for i in r4[keys[0]]:
    assert 'original' in i and 'image' in i and 'confidence' in i
    assert isinstance(i['original'], str)
    assert isinstance(i['image'], str)
    assert isinstance(i['confidence'], int)
def test_garbage_collect():
  __clear_all_caution__('test_db.db')