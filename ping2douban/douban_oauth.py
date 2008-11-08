#coding:utf-8

import time, random, re, hmac, base64
import estutil
from conf import *
from estutil import url_encode_utf8 as escape

def generate_nonce(length=8):
    return ''.join(str(random.randint(0, 9)) for i in range(length))

class douban(object):
    
    comsumer_key = ''
    secret_key = ''
        
    oauth_token_secret = ''
    oauth_token = ''
    
    oauth_realm = API_HOST
    
    def __init__(self, comsumer_key=DOUBAN_API_KEY, secret_key=DOUBAN_SECRET):
        self.comsumer_key = comsumer_key
        self.secret_key = secret_key
    
    def get_normalized_http_url(self, url):
        #TODO: punycode support? haha. Let the oauth guys do it.
        url_re = r'(http://|https://)([\w\.-]*)(:\d+|)(/[^\?]*|)' #well, this regexp costs me hours. TDD rocks
        g = re.search(url_re, url.lower(), re.I)
        r = ''
        if g:
            g=g.groups()
            if (g[0]=='http://' and g[2]==':80') or (g[0]=='https://' and g[2]==':443'):
                r = ''.join([g[0], g[1], g[3]])
            else:
                #FIXME: http:// will be valid.
                r = ''.join(g)
            return r
        else:
            raise Exception('Invalid URL, abort normalize.')
    
    def get_normalized_parameters(self, parameter):
        try:
            del parameter['oauth_signature']
        except:
            pass
        try:
            del parameter['oauth_realm']
        except:
            pass
        key_values = params.items()
        key_values.sort()
        return '&'.join('%s=%s' % (escape(str(k)), escape(str(v))) for k, v in key_values)
    
    def get_signature(self, http_method='GET', url='', oauth_parameter={}, sign_method='HMAC_SHA1'):
        sig = (
                http_method.upper(),
                self.get_normalized_http_url(url),
                estutil.dict2query(oauth_parameter),
            )
        key = escape(self.secret_key) + '&'
        if self.oauth_token_secret:
            key += '&' + escape(oauth_token_secret)
        raw = '&'.join(sig)
        # Got key, raw
        
        if sign_method=='HMAC-SHA1':
            try:
                import hashlib # 2.5
                hashed = hmac.new(key, raw, hashlib.sha1)
            except:
                import sha # deprecated
                hashed = hmac.new(key, raw, sha)
            return base64.b64encode(hashed.digest())
        elif sign_method=='PLAINTEXT':
            return key
        else:
            pass

    def fetch_request_token(self):
        oauth_parameter = {
                            'oauth_consumer_key': self.comsumer_key,
                            'oauth_signature_method': 'PLAINTEXT', #TODO: HMAC-SHA1, RSA-SHA1
                            'oauth_signature': self.secret_key,
                            'oauth_timestamp': str(int(time.time())),
                            'oauth_nonce': generate_nonce(),
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
        print self.secret_key+'&'+ self.oauth_token_secret
        oauth_parameter = {
                            'oauth_consumer_key': self.comsumer_key,
                            'oauth_token': self.oauth_token,
                            'oauth_signature_method': 'PLAINTEXT',
                            'oauth_signature': self.secret_key+'%26'+ self.oauth_token_secret,
                            'oauth_timestamp': str(int(time.time())),
                            'oauth_nonce': generate_nonce(),
                        }
        r = estutil.query2dict(estutil.q(ACCESS_TOKEN_URL, oauth_parameter).read())
        estutil.DEBUG('GOT:\t', r)
        # we got
        # oauth_token_secret=6e5cfba6619453aa&oauth_token=0bcad941e7179c5f23608bc5b546d51d&douban_user_id=1331775
        self.oauth_token_secret = r['oauth_token_secret']
        self.oauth_token = r['oauth_token']
        return r
    
    def q(self, url, content=None, headers={}, method=OAUTH_METHOD):
        oauth_parameter = {
                            'oauth_consumer_key': self.comsumer_key,
                            'oauth_token': self.oauth_token,
                            'oauth_signature_method': method,
                           #'oauth_signature': self.secret_key+'&'+self.oauth_token_secret,
                            'oauth_timestamp': str(int(time.time())),
                            'oauth_nonce': generate_nonce(),
                        }
        oauth_parameter['oauth_signature'] = self.get_signature('POST' if content else 'GET', url, oauth_parameter, method)
        """
        auth_header = 'OAuth '
        for x in range(0, len(oauth_parameter), 2):
            auth_header += oauth_parameter[x] + '="' + oauth_parameter[x+1] + '",'
        auth_header += 'oauth_version="1.0"'
        estutil.DEBUG('Authorization: ' + auth_header)
        headers['Authorization'] = auth_header"""
        print url+'?'+estutil.dict2query(oauth_parameter)
        return estutil.q(url+'?'+estutil.dict2query(oauth_parameter), content, headers)
        
    
    #http://api.douban.com/people/%40me?oauth_consumer_key=012a76168934c0af037f62439b9e420d&oauth_nonce=20518562&oauth_signature=1130f4542d4433f4%266e5cfba6619453aa&oauth_signature_method=PLAINTEXT&oauth_timestamp=1226058002&oauth_token=0bcad941e7179c5f23608bc5b546d51d')
        
        
# content-type是application/json或者application/atom+xml，用xhr提交，
        
# http://api.douban.com/people/1331775/miniblog/contacts?oauth_consumer_key=012a76168934c0af037f62439b9e420d&oauth_token=0bcad941e7179c5f23608bc5b546d51d&oauth_signature_method=PLAINTEXT&oauth_signature=1130f4542d4433f4%266e5cfba6619453aa&oauth_timestamp=1226061298&oauth_nonce=20518562

#  http://api.douban.com/miniblog/saying?oauth_consumer_key=012a76168934c0af037f62439b9e420d&oauth_token=0bcad941e7179c5f23608bc5b546d51d&oauth_signature_method=PLAINTEXT&oauth_signature=1130f4542d4433f4%266e5cfba6619453aa&oauth_timestamp=1226060450&oauth_nonce=20518562
        
    def test2(self):
        miniblog="""<?xml version="1.0" encoding="UTF-8"?><entry xmlns:ns0="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/"><content>测试oAuth</content></entry>"""
        return self.q('http://api.douban.com/miniblog/saying', miniblog, {'Content-Type': 'application/atom+xml'})


        
        
        
        
        
        
        
        
        
        
        
        
        
        
    