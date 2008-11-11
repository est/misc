#coding:utf-8

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app

import conf, douban_oauth, estutil
import hashlib

import logging

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

class Doubaner(db.Model):
    uid = db.StringProperty()
    oauth_token = db.StringProperty()
    oauth_token_secret = db.StringProperty()
    slug = db.StringProperty()


#--------------------------------#
#                                #
#    controller class here?      #
#                                #
#--------------------------------#


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write('Welcome, doubaners! <a href="new">Click</a> to continue.<br />Discuss, feedback, contact the author <a href="http://www.douban.com/group/topic/4604950/">here</a>')

"""<html><head></head>Hey I am here
<form action="pingfm/ac9423e6d78d223b" method="post" accept-charset="utf-8">
<input type="text" name="message" />
<input type="submit" />
</form>
</html>
"""


class NewUser(webapp.RequestHandler):
    """
    One token per user.
    not one token per customer, not one token per request.
    """
    def get(self):
        do = douban_oauth.douban()
            
        base_url = self.request.url[:self.request.url.find(self.request.path)]
        url = do.build_auth_url(base_url+'/finish')
        n = Doubaner(oauth_token=do.oauth_token, oauth_token_secret=do.oauth_token_secret)
        n.put()
        
        self.redirect(url)


class SaveUser(webapp.RequestHandler):
    def get(self):
        #Got redirecte from douban.
        #fetch access token
        token = self.request.get('oauth_token', '')
        if token:
            do = douban_oauth.douban()
            du = Doubaner.all().filter('oauth_token =', token).get()
            
            do.oauth_token = du.oauth_token
            do.oauth_token_secret = du.oauth_token_secret
            
            at = do.fetch_access_token()
            
            token = at['oauth_token']
            secret = at['oauth_token_secret']
            uid = at['douban_user_id']
            
            du.uid = uid
            du.oauth_token = token
            du.oauth_token_secret = secret
            du.slug = new_urn(uid)
            du.put()
        
            
            self.response.headers['Content-Type'] = 'text/html'
            base_url = self.request.url[:self.request.url.find(self.request.path)]
            self.response.out.write('You can now point your ping.fm customized URL to:\t%s' % base_url+'/pingfm/'+du.slug+'<br />')
        else:
            NotFoundPageHandler.get(self)


class Pingfm(webapp.RequestHandler):
    def post(self, slug):
        #TODO: token expired?
        method = self.request.get('method', '')
        title = self.request.get('title', '')
        message = self.request.get('message', '')
        r = Doubaner.all().filter('slug =', slug).get()
        do = douban_oauth.douban(r.oauth_token, r.oauth_token_secret)
        c = '<?xml version="1.0" encoding="UTF-8"?>\
<entry xmlns:ns0="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/">\
<content>%s</content></entry>' % estutil.xml_escape(message)
        logging.info(r.uid+' '+message)
        do.q('http://api.douban.com/miniblog/saying', c, { 'Content-Type': 'application/atom+xml' })
        self.response.out.write('<br />'.join( [x+'='+self.request.get(x, '') for x in self.request.arguments()] ))
        
    def get(self, slug):
        r = Doubaner.all().filter('slug =', slug).get()
        s = ''.join( map( lambda x:x+'='+str(getattr(r, x))+'<br />' ,dir(r) ) )
        self.response.out.write(s)

class ShowUser(webapp.RequestHandler):
    def get(self, uid='1331775'):
        r = Doubaner.all().filter('uid =', uid).get()
        do = douban_oauth.douban(r.oauth_token, r.oauth_token_secret)
        c = do.q('http://api.douban.com/people/%40me').read()
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(c)

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
    ('/new$', NewUser),
    ('/finish$', SaveUser),
    ('/pingfm/(.{16})$', Pingfm),
    ('/u/[^/]*$', ShowUser),
    ('/.*', NotFoundPageHandler),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()