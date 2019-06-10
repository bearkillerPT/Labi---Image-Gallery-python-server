import requests

url = 'http://127.0.0.1:10002/put'
files = {'image': open('./images_to_populate_db/KKs5uvvCPSw.jpg', 'rb')}

r = requests.post(url, files=files)
print(r)
print(r.text)