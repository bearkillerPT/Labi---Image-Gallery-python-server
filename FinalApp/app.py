import cherrypy
from cherrypy import tools
import os
from DbCommunicator import DbCommunicator 
import json
comm = DbCommunicator('app_db.db')

"""This class will not be documented because it's pretty self explanatory"""
class app(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list(self, type = None, name = None, color = None, thr = None, page = None, per_page = None):
        request_body = {} # this form of create dict request will leave all unused parameter empty
        if(type):
            request_body['type'] = type
        if(name):
            request_body['name'] = name
        if(color):
            request_body['color'] = json.loads(color)
        if(thr):
            request_body['thr'] = thr
        if(page):
            request_body['page'] = page
        if(per_page):
            request_body['per_page'] = per_page
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
        return open("./../PastaOndeOGilFazCoisas/class_list.html")
    @cherrypy.expose
    def class_list(self):
        return open("./../PastaOndeOGilFazCoisas/images_list.html")
    @cherrypy.expose
    def images_list(self):
        return open("./../PastaOndeOGilFazCoisas/images_list.html")
    @cherrypy.expose
    def send_images(self):
        return open("./../PastaOndeOGilFazCoisas/send_images.html")
    @cherrypy.expose
    def search_images(self):
        return open("./../PastaOndeOGilFazCoisas/search_images.html")
    @cherrypy.expose
    def about(self):
        return open("./../PastaOndeOGilFazCoisas/about.html")


PATH = os.path.abspath(os.path.dirname(__file__))
config = {
    '/first.html': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.join(PATH, "./../PastaOndeOGilFazCoisas/first.html")
    },
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
