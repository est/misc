#!/usr/bin/env python
#coding:utf-8

import re, sys

try:
    from google.appengine.api  import urlfetch
    GAE = True
except:
    import urllib2
    GAE = False
import random


def DEBUG(*o):
    if DEBUG:
        print ' '.join(map(lambda x:x.encode('gbk', 'ignore') if type(x)==unicode else str(x), o))


def url_encode_utf8(s, safe = ''):
    """
    quoting according to RFC3986
    characters, numbers, '-', '.', '_', '~'
    it's performance is better than `urllib.quote`
    """
    safe_re = re.compile('([^\w' + re.escape(safe + ';/?:@&=+$,-.~') + '])')
    if type(s)==unicode:
        r = s.encode('utf-8')
    else:
        r = str(s).decode('gbk', 'replace').encode('utf-8')
    return safe_re.sub(lambda x:'%%%02X' % ord(x.group(0)) , r)

def unquote(s):
    return re.sub('%[a-fA-F0-9]{2}', lambda x: chr(int(x.group()[1:], 16)), s)

def q(url, content=None, headers={}):
    """
    GET/POST an URL, compatible with GAE
    you must manually encode Headers
    """
    if type(content) == dict:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        content = dict2query(content)
    DEBUG('QRY:\t', url, '\n\t', content)
    if GAE:
        return urlfetch.fetch(url, content, method=GET if content==None else POST, headers=headers)
    else:
        r = urllib2.Request(url, content)
        for x in headers:
            r.add_header(x, headers[x])
        return urllib2.urlopen(r)
    

def new_slug(length=5):
    keys='23456789abcdefghjkmnpqrstuvwxyz'
    return ''.join(random.choice(keys) for x in range(length))


def query2dict(s):
    """
    unpack a cgi query string to a dict structure, decoding.
    /search?q=this+is+a+test the plus sign will not be changed.
    if mbcs characters were utf-8 encoded, decode it your self.
    """
    return dict(map(lambda x:map(lambda x:unquote(x), x.split('=')), s.split('&')))

def dict2query(d, escape=True, sort=True):
    k = d.items()
    k.sort()
    encode = url_encode_utf8 if escape else lambda x:x
    r = '&'.join('%s=%s' % (encode(i), encode(j)) for i,j in (k if sort else map(lambda x:(x,d[x]), d)))
    print r
    return r






