from math import ceil
from time import strftime, localtime
from cgi import parse_qs
from os import listdir
from os.path import isfile, join, getctime

import cv2
import skimage

# Displays the images given in the directory "path".
# For pagination to work properly, images should have a timestamp in the filename, as the list is ordered by the filename.

path_to_images = "/var/www/camera/camera_pics"
page_size = 50

def list_images(path, page):
   start_image = page * page_size;
   # Get image list, sorted by filename.
   image_paths =[join(path ,f) for f in listdir(path) if isfile(join(path, f))]
   image_paths.sort()
   # Get sublist of images for current page.
   image_paths_sublist = image_paths[start_image:start_image + page_size]
   html_images = [ "<a href='" + s[16:] + "' ><img src='" + s[16:] + "' width=200 /></a>" for s in image_paths_sublist]
   pages = ceil(len(image_paths)/50)
   # Display link for every 50 images, show ctime of the first of those images.
   page_links = [ "<a href='?page=0'>[" + strftime("%Y-%m-%d %H:%M",localtime(getctime(image_paths[1]))) + "]</a>" ]
   if pages > 1:
      page_links.extend([ "<a href='?page=" + str(x) + "'>[" + strftime("%Y-%m-%d %H:%M",localtime(getctime(image_paths[x*50-49]))) + "]</a>" for x in range(1,pages) ])

   output = " ".join(html_images) \
            + "<p> Total: " + str(len(image_paths)) + "</p>" \
            + "<p> Showing: " + str(start_image + 1) + "-" + str(start_image + page_size) + "</p>" \
            + " ".join(page_links)
   return output

def application(environ, start_response):
    status = '200 OK'
    get_params = parse_qs(environ['QUERY_STRING'])
    page = int(get_params.get("page")[0]) if get_params.get("page") != None else 0
    output = bytes(list_images(path_to_images, page), "UTF-8")
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


