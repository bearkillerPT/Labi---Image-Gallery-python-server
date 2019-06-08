import cherrypy
from hashlib import md5
from cherrypy import tools
import os
from DbCommunicator import DbCommunicator 
import json
comm = DbCommunicator('app_db.db')
"""A maioria dos testes à funções desta class são um teste direto à API"""
"""This class will not be documented because it's pretty self explanatory"""
class app(object):
    """O teste deste metodo é muito semelhante ao do request na outra classe, só tens de o fazer na forma de GET
    e POST request em vez de chamada a uma função python diretamente, depois da explicação no discord em principio
    entendes exatamente o que fazer aqui"""
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list(self, type = None, name = None, color = None, thr = None, page = None, per_page = None):
        request_body = {} # this way of create dict request will leave all unused parameter empty
        if(type):
            request_body['type'] = type #type é uma palavra reservada, apesar disso não há erros
        if(name):
            request_body['name'] = name
        if(color):
            request_body['color'] = json.loads(color)
        if(thr):
            request_body['thr'] = float(thr)
        if(page):
            request_body['page'] = page
        if(per_page):
            request_body['per_page'] = per_page
        result = comm.request(request_body)
        print(result)
        return result

    """Muito parecido com o teste à funcção add/request/get da outra classe só que via POST request"""
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def put(self, image):
        img = image.file.read()
        result = [comm.request({'put':{'image':img}})]
        print(result)
        name = md5(img).hexdigest()
        result.append(comm.get(name))
        return result

    """
        Igual ao da função get mas via GET request
    """
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def get(self, id):
        result = comm.get(id)
        print(result)
        return result

    """Testar se recebes uma file quando acedes ao site.name/index"""
    @cherrypy.expose
    def index(self):
        return open("./../FrontEnd/class_list.html")


PATH = os.path.abspath(os.path.dirname(__file__))
config = {
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, "./../FrontEnd")
    },
    '/images': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, "images")
    },
    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, "./../FrontEnd/js")
    },
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, "./../FrontEnd/css")
    }
}

cherrypy.config.update({'server.socket_host': '127.0.0.1',
                        'server.socket_port': 10002,
                       })
cherrypy.quickstart(app(),'/',config=config)
