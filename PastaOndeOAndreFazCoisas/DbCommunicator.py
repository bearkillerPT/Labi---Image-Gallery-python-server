import sqlite3
from hashlib import md5
import requests
import sys
from PIL import Image
import io
from os import remove 
from urllib.request import Request, urlretrieve 
class DbCommunicator:
  def __init__(self, db_name: str) -> None:
    self.db_name = db_name

  def get_dims_and_color(self, image_path: str) -> tuple:
    img = Image.open(image_path)
    width, height = img.size
    total_pixel_count = width * height
    avg_color = {'r':0,'g':0,'b':0}
    for x in range(width):
      for y in range(height):
        p = img.getpixel((x,y))
        avg_color['r'] += p[0]/total_pixel_count
        avg_color['g'] += p[1]/total_pixel_count
        avg_color['b'] += p[2]/total_pixel_count
    avg_color['r'] = round(avg_color['r'])
    avg_color['g'] = round(avg_color['g'])
    avg_color['b'] = round(avg_color['b'])
    return (height, width, (avg_color['r'], avg_color['g'], avg_color['b']))


  def request_caracteristics(self, image: bytearray, name, threshold) -> dict:
    session = requests.Session()
    url = "http://image-dnn-sgh-jpbarraca.ws.atnog.av.it.pt/process"
    file = {'img': image}
    r = session.post(url=url, files=file, data=dict(thr=0)) # thr = 0 para que sejam devolvidas todas as classes
    img_dict = None
    if r.status_code == 200:
      img_dict= r.json()
    else:
      return('Connection Failed')
    caracts = []
    for i in img_dict:
      caracts.append({'name' :name, 'class': i['class'],
                      'box':(i['box']),
                      'confidence':i['confidence']})
    return caracts

  def add(self, image: bytearray):
    db = sqlite3.connect(self.db_name)
    name = md5(image).hexdigest()
    already_in_db = db.execute(
      'select * from Imagens where image_path = ? ;',(str(name),)
    ).fetchall()
    if(already_in_db):
      return("Image Already in Database")
    caracts = self.request_caracteristics(image, name, '')
    if(len(caracts) == 0):
      return("Any class detected")
    

    f1 = open("./images/" + name, 'wb+')
    f1.write(image)
    f1.close()
    height, width, color = self.get_dims_and_color("./images/" + name)
    db.execute("insert into Imagens values (?, ?, ?, ?, ?, ?);", (name, height, width, color[0],color[1],color[2],))
    cropper = Image.open(io.BytesIO(image))
    for i in caracts:
      cropped = cropper.crop((
        i['box']['x'],i['box']['y'],
        i['box']['x1'],i['box']['y1'],)
        )
      imgByteArr = io.BytesIO()
      cropped.save(imgByteArr, 'png')
      imgByteArr = imgByteArr.getvalue()
      cropped_name = md5(imgByteArr).hexdigest()
      f = open("./images/" + cropped_name, 'wb+')
      f.write(imgByteArr)
      f.close()
      cropped_width, cropped_height, cropped_color = self.get_dims_and_color("./images/" + cropped_name)
      db.execute("insert into Imagens values (?, ?, ?, ?, ?, ?);",
                (cropped_name, cropped_height, cropped_width, cropped_color[0],cropped_color[1],cropped_color[2],))
      db.execute('insert into RelImgCaract (FKOriginalImageName, FKCroppedImageName,'+ 
                'CaractName , Box, Confidence) values (?,?,?,?,?);'
                ,(name, cropped_name, i['class'],
                str(i['box']['x']) + "," + str(i['box']['y']) + "," + str(i['box']['x1']) + "," + str(i['box']['y1']),
                i['confidence']))
    db.commit()
    db.close()
    return("Image Added successfully")

  def remove(self, img_object: dict):
    db = sqlite3.connect(self.db_name)
    img_name = ""
    if('image' in img_object):
      img_name = md5(img_object['image']).hexdigest()
    elif('image_name' in img_object):
      img_name = img_object['image_name']
    else:
      return("Bad Call")
    r = db.execute("delete from Imagens where image_path = ?;",(img_name,)).fetchall()
    if(r):
      return("Image does not exist in database")
    remove("./images/" + img_name)
    files_to_delete_name = db.execute("select FKCroppedImageName from RelImgCaract where FKOriginalImageName = ?;",(img_name,)).fetchall()
    db.execute("delete from RelImgCaract where FKOriginalImageName = ?;",(img_name,))
    for i in files_to_delete_name:
      remove("./images/" + i[0])
    db.commit()
    db.close()
    return("Image removed successfully")

  def request(self, request_obj: dict):
    data = []
    db = sqlite3.connect(self.db_name)
    result = "Bad Call"
    if('put' in request_obj):
      if('image' in request_obj['put']):
        self.add(request_obj['put']['image'])
      elif('uri' in request_obj['put']):
        req = Request(request_obj['put']['uri'], headers={'User-Agent': 'Mozilla/5.0'})
        f = urlretrieve(req)
        self.add(open(f, 'rb').read())
    elif('type' in request_obj and 'name' in request_obj and 'color' in request_obj and request_obj['type'] == 'detected'):
      results = db.execute(
      "select FKOriginalImageName, FKCroppedImageName, Confidence from RelImgCaract "+
      "inner join Imagens on RelImgCaract.FKCroppedImageName = Imagens.image_path where CaractName = ?  and "+
      "(R - ?) * (R - ?) + (G - ?) * (G - ?) + (B - ?) * (B - ?) < ?" ,
      (
        request_obj['name'],
        request_obj['color']['R'],
        request_obj['color']['R'],
        request_obj['color']['G'],
        request_obj['color']['G'],
        request_obj['color']['B'],
        request_obj['color']['B'],
        request_obj['color']['tol'] * 195075, #denormalização , numero max 
      ) 
      ).fetchall()
      result = {request_obj['name']:[{'original':i[0],'image':i[1],'confidence':round(i[2] * 100)} for i in results]}
    
    elif('type' in request_obj and 'name' in request_obj and request_obj['type'] == 'detected'):
      results = db.execute(
      "select FKOriginalImageName, FKCroppedImageName, Confidence from RelImgCaract where CaractName = ? ",
      (request_obj['name'],) 
      ).fetchall()
      result = {request_obj['name']:[{'original':i[0],'image':i[1],'confidence':round(i[2] * 100)} for i in results]}
    
    elif('type' in request_obj):
      if(request_obj['type'] == 'names'):
        result = db.execute("select distinct CaractName from RelImgCaract").fetchall()
        result = [i[0] for i in result]
      elif(request_obj['type'] == 'detected'):
        names = db.execute("select distinct CaractName from RelImgCaract").fetchall()
        names = [i[0] for i in names]
        result = {}
        for name in names:
          results = db.execute(
          "select FKOriginalImageName, FKCroppedImageName, Confidence from RelImgCaract where CaractName = ? ",
          (name,) 
          ).fetchall()
          result[name] = [{'original':i[0],'image':i[1],'confidence':round(i[2] * 100)} for i in results]
    db.commit()
    db.close()
    return(result)

  def __clear_all_caution__(self):
    db = sqlite3.connect('app_db.db')
    db.execute('delete from RelImgCaract where true')
    db.execute('delete from Imagens where true')
    db.commit()
    db.close()


if __name__ == '__main__':
  comm = DbCommunicator('app_db.db')
  # comm.__clear_all_caution__()
  print(comm.add(open('image.jpg', 'rb').read()))
  print(comm.add(open('image2.jpg', 'rb').read()))
  print(comm.add(open('image3.jpeg', 'rb').read()))
  print(comm.request(
    {
      'put' : {
        #'image': open('image.jpg', 'rb').read(), 
        'uri' : 'https://webcuriosos.com.br/wp-content/uploads/2017/06/DESAFIO-Voc%C3%AA-consegue-encontrar-os-erros-nestas-fotos-768x399.jpg'
        },
      'type' : 'detected', 
      'name' : 'person', 
      'color' : {'R':255,'G':255,'B':255,'tol':0,}
    }
  ))