import sqlite3
from hashlib import md5
import requests
import sys
from PIL import Image
import io
from os import remove 
from urllib.request import urlretrieve 
import os
import random
class DbCommunicator:
  """Convém que todos os testes sejam parametrizaveis em numero e randomicos em conteudo
  ou seja, as imagens escolhidas para o teste são aleatorias e o numero de imagens escolhidas é 
  parametrizavel. Exemplo, defines variavel de quantidade de testes assim 'NUMTESTS = int(numero qlquer)'
  e a chamada às funções de teste começa com um 'for i in range(NUMTESTS):'. No interior dos testes
  escolhes uma imagem aleatoria, recomendo que cries uma lista com todas as imagens possiveis
  e uses a função random.choice(listaDeImages) para aleatorizar a imagem do current test  """
  """Esta função não precisa de testes"""

  """Na maioria dos metodos é uma boa ideia testar casos com chamadas errada, tipo passar uma chamada errada para a função"""
  def __init__(self, db_name: str) -> None:
    """Initializes the object that will connect to the given database"""
    self.db_name = db_name

  """O teste consiste em enviar algumas imagens para a função e verificar 
  o tipo e coerencia dos outputs, com coerencia refiro me às avg_colors que deverão 
  ser cada uma delas um numero entre 0 e 255"""
  def get_dims_and_color(self, image_path: str) -> tuple:
    """Collects image average color and dimensions that will be added to the database"""
    img = Image.open(image_path)
    width, height = img.size
    total_pixel_count = width * height
    img2 = img.resize((1, 1))
    color = img2.getpixel((0, 0))
    avg_color = {'r':color[0],'g':color[1],'b':color[2]}
    return (height, width, (avg_color['r'], avg_color['g'], avg_color['b']))


  """Igual à função de cima, passas um bytearray para a função, podes obter um bytearray a 
  partir de um path desta maneira open(path,'rb').read(). Depois verificas os tipos dos outputs
  e a sua coerencia, o output é uma lista de dicionarios, em cada dicionario o name é uma string com
  comprimento igual ao de um hash md5, a class é uma string, a box é um dicionario com 4 atributos inteiros
  x,x1,y,y1 e a confiança é real um valor entre 0 e 1 """
  def request_caracteristics(self, image: bytearray, name: str) -> list:
    """Requests caracteristics of image from the given api"""
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
  """
  Neste metodos os testes são algo complexos, envias uma imagem como bytearray e depois testas se
  O output é: 
  'Image Already in Database', neste caso procedes para os testes à database,
  'Any class detecter', neste caso paras o teste por aqui,
  'Image Added Successfully', neste caso procedes para os testes à db,
  Os testes à db consiste em ligares à db e procurares com o comando 
  Select * from RelImgCaracts where FKOriginalImage = ?, hashMd5DoConteudoDaImages
  caso nada seja encontrado, o teste falha, caso seja encontrado, o teste prossegue
  depois pegas no resultado, nas FKOriginalImage e nas FKCroppedImage (<- not rly sure se 
  é exatamente este o nome, vê o schema da table)
  e pesquisas por ela na tabela Imagens da db, se existir sempre resultado, há sucesso no teste
  """
  def add(self, image: bytearray):
    """Adds a new item item to database collection of images, the image provided can generate multiple new images stored
    if there are multiple classes found in it, the respective bounding box will also be stored"""
    db = sqlite3.connect(self.db_name)
    name = md5(image).hexdigest()
    already_in_db = db.execute(
      'select * from Imagens where image_path = ? ;',(str(name),)
    ).fetchall()
    if(already_in_db):
      return("Image Already in Database")
    caracts = self.request_caracteristics(image, name)
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
  """
  O teste deste metodo é parecido com o do add mas neste caso o teste têm sucesso caso nada seja encontrado na db
  quando pesquisas pelo hash md5 do conteudo das imagens
  """
  def remove(self, img_object: dict):
    """Removes an item from the database, either a child image or a parent, if it is a parent image all childs will be deleted"""
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

  """
    Testar coerencia dos resultados mais uma vez
  """
  def get(self, id: str):-> 
    """Retrieves an image based on an id specified on the request"""
    db = sqlite3.connect(self.db_name)
    db_request = db.execute("select FKOriginalImageName, FKCroppedImageName, CaractName , Box, Confidence from RelImgCaract"+
    " where FKOriginalImageName = ? or FKCroppedImageName = ?;",
    (id,id,)).fetchall()
    if(len(db_request) == 0): result = "Image Not Found"
    else:
      result = [{
        'original':i[0],
        'image':i[1],
        'class':i[2],
        'box':{
          'x':i[3].split(',')[0],
          'y':i[3].split(',')[1],
          'x1':i[3].split(',')[2],
          'y1':i[3].split(',')[3]
        },
        'confidence':round(i[4]*100)} for i in db_request]
    db.commit()
    db.close()
    return(result)
  """Este metodo provavelmente é mais simples explicar por discord isto é um bocado code heavy principalmente se n
  estás à vontade com GET e POST requests nem com python no geral"""
  def request(self, request_obj: dict):
    """Parses the request made via GET and retrieves the asked data"""
    data = []
    db = sqlite3.connect(self.db_name)
    result = "Bad Call"
    per_page = 10
    page = 1
    if('per_page' in request_obj):
      per_page = int(request_obj['per_page'])
    
    if('page' in request_obj):
      page = int(request_obj['page'])

    if('put' in request_obj):
      if('image' in request_obj['put']):
        result = self.add(request_obj['put']['image'])
      elif('uri' in request_obj['put']):
        try:
          f = urlretrieve(request_obj['put']['uri'])[0]
          result = self.add(open(f, 'rb').read())
        except:
          result = "required link is forbiden"
    elif('type' in request_obj and 'name' in request_obj and 'color' in request_obj and request_obj['type'] == 'detected'):
      if ('thr' in request_obj): thr = request_obj['thr'];  
      else: thr = 0
      results = db.execute(
      "select FKOriginalImageName, FKCroppedImageName, Confidence from RelImgCaract "+
      "inner join Imagens on RelImgCaract.FKCroppedImageName = Imagens.image_path where CaractName = ? and Confidence > ? and "+
      "(R - ?) * (R - ?) + (G - ?) * (G - ?) + (B - ?) * (B - ?) < ? limit ? offset ?" ,
      (
        request_obj['name'],
        thr,
        request_obj['color']['R'],
        request_obj['color']['R'],
        request_obj['color']['G'],
        request_obj['color']['G'],
        request_obj['color']['B'],
        request_obj['color']['B'],
        request_obj['color']['tol'] * 195075, #  , numero max 
        per_page,
        (page - 1) * per_page,
      ) 
      ).fetchall()
      result = {request_obj['name']:[{'original':i[0],'image':i[1],'confidence':round(i[2] * 100)} for i in results]}
      
    elif('type' in request_obj and 'name' in request_obj and request_obj['type'] == 'detected'):
      if ('thr' in request_obj): thr = request_obj['thr'];  
      else: thr = 0
      results = db.execute(
      "select FKOriginalImageName, FKCroppedImageName, Confidence from RelImgCaract where CaractName = ? and Confidence > ? limit ? offset ?",
      (
        request_obj['name'],
        thr,
        per_page,
        (page - 1) * per_page,
      ))
      results = results.fetchall()
      result = {request_obj['name']:[{'original':i[0],'image':i[1],'confidence':round(i[2] * 100)} for i in results]}
    
    elif('type' in request_obj):
      if(request_obj['type'] == 'names'):
        result = db.execute("select distinct CaractName from RelImgCaract").fetchall()
        result = [i[0] for i in result]
      elif(request_obj['type'] == 'detected'):
        
        result = {}
        results = db.execute(
        "select FKOriginalImageName, FKCroppedImageName, Confidence, CaractName from RelImgCaract limit ? offset ?",
        (
          per_page,
          (page - 1) * per_page,
        )
        ).fetchall()
        result = [{'original':i[0],'image':i[1],'confidence':round(i[2] * 100),'class':i[3]} for i in results]
    db.commit()
    db.close()
    return(result)


"""Both functions bellow are for debugging purposes and will not be exported to app.py"""

def __clear_all_caution__():
  """Clears database, used for upload size purposes"""
  db = sqlite3.connect('app_db.db')
  db.execute('delete from RelImgCaract')
  db.execute('delete from Imagens')
  db.commit()
  db.close()
  for filename in os.listdir("./images"):
    remove("./images/" + filename)
  f = open("./images/fileParaOGitNApagarAPasta.kmn", 'w')
  f.write("yhey")
  f.close()


def populate(comm):
  """Repopulate database with some predefined images, used for deploy purposes"""
  for filename in os.listdir("./images_to_populate_db"):
    print(filename)
    print(comm.add(open('./images_to_populate_db/' + filename, 'rb').read()))


"""Deploy code"""
if __name__ == '__main__':
  if(sys.argv[1] == 'c'):
    __clear_all_caution__()
  elif(sys.argv[1] == 'p'):
    populate(DbCommunicator('app_db.db'))
  #populate(DbCommunicator('app_db.db'))
