import requests

url = 'http://127.0.0.1:8080/put'
files = {'image': open('image3.jpeg', 'rb')}

r = requests.post(url, files=files)
print(r)
print(r.text)