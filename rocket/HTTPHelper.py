
import urllib2
import base64

import Config

def read_url(url):
  request = urllib2.Request(url)

  if Config.HTTPAUTH_USER and Config.HTTPAUTH_PASS:
    authstring = base64.encodestring('%s:%s' % (Config.HTTPAUTH_USER, Config.HTTPAUTH_PASS))
    authstring = authstring.replace('\n', '')
    request.add_header("Authorization", "Basic %s" % authstring)

  return urllib2.urlopen(request).read()

