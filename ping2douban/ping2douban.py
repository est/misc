#coding:utf-8

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import conf
import hashlib

import douban_oauth

#--------------------------------#
#                                #
#        dummy functions         #
#                                #
#--------------------------------#


def new_urn(userid):
    #Use another algorithm? map user_id to another namespace with salt?
    return hashlib.md5(userid+conf.URN_SALT).hexdigest()[9:25]

#--------------------------------#
#                                #
#        dummy db modules        #
#                                #
#--------------------------------#

class Doubaner(db.model):
    uid = db.StringProperty(required=True)
    oauth_token = db.StringProperty(required=True)
    oauth_token_secret = db.StringProperty(required=True)
    slug = db.StringProperty(requried=True)


#--------------------------------#
#                                #
#    controller class here?      #
#                                #
#--------------------------------#


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hey I am here'+"\n")


class NewUser(webapp.RequestHandler):
    """
    One token per user.
    not one token per customer, not one token per request.
    """
    def post(self):
        existing = False
        if existing:
        #already in database, show URL, re-oauth
            pass
        else:
        #new user, negotiate with douban
            oauth = douban_oauth.douban()
            token = oauth.request_token()
            #save token to db
        self.redirect(conf.AUTHORIZATION_URL)


class SaveUser(webapp.RequestHandler):
    def get(self):
        #Got redirecte from douban.
        #fetch access token
        
        douban_oauth.fetch_access_token()
        
        self.response.headers['Content-Type'] = 'text/html'
        douban_user_id = self.request.get('douban_user_id')
        url = self.request.url[:self.request.url.find('/', 8)] + '/u/' + new_urn(douban_user_id)
        self.response.out.write('You can now point your ping.fm customized URL to:\t%s' % url)


class Pingfm(webapp.RequestHandler):
    def post(self):
        #TODO: token expired?
        method = self.request.get('method', '')
        title = self.request.get('title', '')
        message = self.request.get('message', '')


#--------------------------------#
#                                #
#      URL Re-write router       #
#                                #
#--------------------------------#



class NotFoundPageHandler(webapp.RequestHandler):
    def get(self):
        self.error(404)
        self.response.out.write('<h1>A better 404?</h1>')


application = webapp.WSGIApplication([
                                        ('/', MainPage),
                                       #('/oauth', oAuth),
                                        ('/create.*$', NewUser),
                                        ('/finish.*$', SaveUser),
                                        ('/pingfm.*$', Pingfm),
                                        
                                        ('/.*', NotFoundPageHandler),
                                    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()