from PIL import Image
import os
from os.path import basename

def reduce_size(category, filename):
  #basename=os.path.basename(path)
  source = 'media1/' + category + '/' + filename
  destination = 'media/books/' + category + '/' + filename
  basewidth = 250
  img = Image.open(source)
  #print img
  wpercent = (basewidth/float(img.size[0]))
  hsize = int((float(img.size[1])*float(wpercent)))
  img = img.resize((basewidth,hsize), Image.ANTIALIAS)
  img.save(destination, optimize=True, quality=60)
  print source + "  ---> Processed"
  #return img


def process_data(category, path_to_dir):
  images = os.listdir(path_to_dir)
  for image in images:
    reduce_size(category, image)

