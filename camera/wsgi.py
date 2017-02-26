
from os import listdir
from os.path import isfile, join

path_to_images = "/var/www/camera/camera_pics"

def list_images(path):
   image_paths =[join(path ,f) for f in listdir(path) if isfile(join(path, f))]
   html_images = [ "<a href='" + s[16:] + "' ><img src='" + s[16:] + "' width=100 height=100 /></a>" for s in image_paths]
   return " ".join(html_images)

def application(environ, start_response):
    status = '200 OK'
    output = bytes(list_images(path_to_images), "UTF-8")
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
