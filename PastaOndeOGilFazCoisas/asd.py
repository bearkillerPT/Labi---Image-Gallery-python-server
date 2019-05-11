import cherrypy
from cherrypy import tools

PATH = os.path.abspath(os.path.dirname(__file__))
config = {
    '/':{
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : os.path.join(PATH)
    }
}
cherrypy.quickstart(app(),'/',config=config)