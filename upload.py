#!/opt/local/bin/python2.5

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Upload(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render('upload.html',{}))

application = webapp.WSGIApplication([
  ('/', Upload)
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
