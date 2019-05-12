import cherrypy
from cherrypy import tools
import os
from DbCommunicator import DbCommunicator 
import json
comm = DbCommunicator('app_db.db')


class app(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list(self, type = None, name = None, color = None, thr = None):
        request_body = {} # this form of create dict request will leave all unused parameter empty
        if(type):
            request_body['type'] = type
        if(name):
            request_body['name'] = name
        if(color):
            request_body['color'] = json.loads(color)
        if(thr):
            request_body['thr'] = thr
        result = comm.request(request_body)
        print(result)
        return result

    @cherrypy.expose
    def put(self, image):
        result = comm.request({'put':{'image':image.file.read()}})
        print(result)
        return result

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def get(self, id):
        result = comm.get(id)
        print(result)
        return result

    @cherrypy.expose
    def index(self):
        return open("./../PastaOndeOGilFazCoisas/index.html")


PATH = os.path.abspath(os.path.dirname(__file__))
config = {
    '/images': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, "images")
    },
    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, "./../PastaOndeOGilFazCoisas/js")
    },
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, "./../PastaOndeOGilFazCoisas/css")
    }
}


cherrypy.quickstart(app(),'/',config=config)
