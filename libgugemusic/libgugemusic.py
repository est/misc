#!/usr/bin/env python
#code:utf-8

__doc__ = """
See introduction here:
http://initiative.yo2.cn/archives/639811
"""

import re, hashlib
from urllib import unquote as url_unquote

try:
    import urllib2
except:
    pass


#extracted from http://www.gstatic.cn/top100/player/2166974035-OnlinePlayer.swf
PLAYER_KEY = 'eca5badc586962b6521ffa54d9d731b0' 

def download_mp3_by_id(id, q=urllib2.urlopen):
    """download .mp3 of the given id"""
    r = re.search(  '<a href="/music/top100/url\?q=(http%3A%2F%2Ffile.*\.mp3)', 
                    q('http://www.google.cn/music/top100/musicdownload?id=' + id).read() )
    if r:
        return url_unquote(r.groups()[0])
    else:
        return ''

def stream_mp3_by_id(id, q=urllib2.urlopen):
    """extract songUrl, lyricsUrl, albumThumbnailLink, label, providerId of a given id"""
    r = q(  'http://www.google.cn/music/songstreaming?id=' + id +
            '&client=&output=xml&sig=' + hashlib.md5(PLAYER_KEY + id).hexdigest() + '&cad=pl_player' ).read()
    d = {}
    for x in ['songUrl', 'lyricsUrl', 'albumThumbnailLink', 'label', 'providerId']:
        p = re.search('<'+x+'>([^<]*)</'+x+'>', r ) #not using xml.sax.saxutils.(un)escape for laziness
        if p:
            d[x] = p.groups()[0] #assume Google always respond in UTF-8
    return d
