#!/opt/local/bin/python25

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import images
from google.appengine.ext import db

class DbImage(db.Model):
  image = db.BlobProperty()

class Convert(webapp.RequestHandler):
  def post(self):
    raw_image = self.request.get('image')
    key = self.request.get('key')
    if raw_image:
      image = images.Image(raw_image)
    elif key:
      image = images.Image(DbImage.get(key).image)

    output_size = self.request.get('output_size')
    left = self.request.get('left')
    top = self.request.get('top')
    select_size = self.request.get('select_size')
    image.crop(float(left)/float(image.width), float(top)/float(image.height), (float(left)+float(select_size))/float(image.width), (float(top)+float(select_size))/float(image.height))
    image.resize(int(output_size), int(output_size))
    image.im_feeling_lucky()
    output_image = image.execute_transforms(output_encoding=images.PNG)
    db_image = DbImage()
    db_image.image = db.Blob(output_image)
    key = db_image.put()
    self.redirect('/convert?key=%s' % key)

  def get(self):
    key = self.request.get('key')
    self.response.out.write(template.render('convert.html',{'key':key}))

class Upload(webapp.RequestHandler):
  def get(self):
    key = self.request.get('key')
    self.response.out.write(template.render('upload.html',{'key':key}))

  def post(self):
#     image = images.Image(self.request.get('image'))
#     output_image = image.execute_transforms(images.PNG)
    db_image = DbImage()
    db_image.image = db.Blob(self.request.get('image'))
    key = db_image.put()
    self.redirect('/upload?key=%s' % key)

class Index(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render('index.html',{}))

class Image(webapp.RequestHandler):
  def get(self):
    key = self.request.get('key')
    db_image = DbImage.get(key)
    if db_image.image:
      self.response.headers['Content-Type'] = "image/png"
      self.response.out.write(db_image.image)
    else:
      self.error(404)

application = webapp.WSGIApplication([
  ('/convert', Convert),
  ('/upload', Upload),
  ('/image', Image),
  ('/', Index)
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
