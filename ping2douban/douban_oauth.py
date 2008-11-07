#coding:utf-8

import time, random, re
import estutil
from conf import *

def generate_nonce(length=8):
    return ''.join(str(random.randint(0, 9)) for i in range(length))

class douban(object):
    
    comsumer_key = ''
    secret_key = ''
    
    oauth_method = OAUTH_METHOD
        
    oauth_token_secret = ''
    oauth_token = ''
    
    oauth_realm = API_HOST
    
    oauth_timestamp = str(int(time.time()))

    oauth_nonce = generate_nonce()
    
    def __init__(self, comsumer_key=DOUBAN_API_KEY, secret_key=DOUBAN_SECRET):
        self.comsumer_key = comsumer_key
        self.secret_key = secret_key
    
        
    def fetch_request_token(self):
        oauth_parameter = {
                            'oauth_consumer_key': self.comsumer_key,
                            'oauth_signature_method': self.oauth_method, #TODO: HMAC-SHA1, RSA-SHA1
                            'oauth_signature': self.secret_key,
                            'oauth_timestamp': self.oauth_timestamp,
                            'oauth_nonce': self.oauth_nonce,
                        }
        r = estutil.q(REQUEST_TOKEN_URL, oauth_parameter).read()
        estutil.DEBUG('GOT:\t', r)
        # should return something like
        # oauth_token=ab3cd9j4ks73hf7g&oauth_token_secret=xyz4992k83j47x0b
        d = estutil.query2dict(r)
        self.oauth_token_secret = d['oauth_token_secret']
        self.oauth_token = d['oauth_token']
        return self.oauth_token, self.oauth_token_secret
    
    def auth_in_browser(self):
        oauth_token, oauth_token_secret = self.fetch_request_token()
        estutil.DEBUG(oauth_token_secret, oauth_token)
        import webbrowser
        return webbrowser.open(AUTHORIZATION_URL + '?oauth_token=' + oauth_token)
    
    def fetch_access_token(self):
        oauth_parameter = {
                            'oauth_consumer_key': self.comsumer_key,
                            'oauth_token': self.oauth_token,
                            'oauth_signature_method': self.oauth_method,
                            'oauth_signature': self.secret_key+'&'+ self.oauth_token_secret,
                            'oauth_timestamp': self.oauth_timestamp,
                            'oauth_nonce': self.oauth_nonce,
                        }
        r = estutil.query2dict(estutil.q(ACCESS_TOKEN_URL, oauth_parameter).read())
        estutil.DEBUG('GOT:\t', r)
        # we got
        # oauth_token=ab3cd9j4ks73hf7g&oauth_token_secret=xyz4992k83j47x0&douban_user_id=sakinijino
        self.oauth_token_secret = r['oauth_token_secret']
        self.oauth_token = r['oauth_token']
        return r
    
    def q(self, url, content=None, headers={}):
        oauth_parameter = {
                            'oauth_consumer_key': self.comsumer_key,
                            'oauth_token': self.oauth_token,
                            'oauth_signature_method': self.oauth_method,
                            'oauth_signature': self.secret_key+'&'+self.oauth_token_secret,
                            'oauth_timestamp': self.oauth_timestamp,
                            'oauth_nonce': self.oauth_nonce,
                        }
        """
        auth_header = 'OAuth '
        for x in range(0, len(oauth_parameter), 2):
            auth_header += oauth_parameter[x] + '="' + oauth_parameter[x+1] + '",'
        auth_header += 'oauth_version="1.0"'
        estutil.DEBUG('Authorization: ' + auth_header)
        headers['Authorization'] = auth_header"""
        return estutil.q(url, content, headers)
        
    
    def test(self):
        return estutil.q('http://api.douban.com/people/%40me')
        
    def test2(self):
        miniblog="""<?xml version='1.0' encoding='UTF-8'?><entry xmlns:ns0="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/"><content>测试oAuth</content></entry>"""
        return estutil.q('http://api.douban.com/miniblog/saying?oauth_consumer_key=012a76168934c0af037f62439b9e420d&oauth_nonce=20518562&oauth_signature=1130f4542d4433f4%266e5cfba6619453aa&oauth_signature_method=PLAINTEXT&oauth_timestamp=1226058002&oauth_token=0bcad941e7179c5f23608bc5b546d51d', estutil.dict2query({
                            'oauth_consumer_key': self.comsumer_key,
                            'oauth_token': self.oauth_token,
                            'oauth_signature_method': self.oauth_method,
                            'oauth_signature': self.secret_key+'&'+self.oauth_token_secret,
                            'oauth_timestamp': self.oauth_timestamp,
                            'oauth_nonce': self.oauth_nonce,
                        })+'\n'+miniblog, {'Content-Type': 'text/xml'})

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    