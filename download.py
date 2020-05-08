from os.path import basename
from urlparse import urlsplit
import urllib2

def url2name(url):
  return basename(urlsplit(url)[2])

def download(url, localFileName = None):
  proxy_support = urllib2.ProxyHandler({'http:':'127.0.0.1:1080'})
  opener = urllib2.build_opener(proxy_support)
  urllib2.install_opener(opener)
  localName = url2name(url)
  req = urllib2.Request(url)
  r = urllib2.urlopen(req)
  if r.info().has_key('Content-Disposition'):
    # If the response has Content-Disposition, we take file name from it
    localName = r.info()['Content-Disposition'].split('filename=')[1]
    if localName[0] == '"' or localName[0] == "'":
      localName = localName[1:-1]
  elif r.url != url:
    # if we were redirected, the real file name we take from the final URL
    localName = url2name(r.url)
  if localFileName:
    # we can force to save the file as specified name
    localName = localFileName
  f = open(localName, 'wb')
  f.write(r.read())
  f.close()

download(r'https://maven.google.com/com/android/support/appcompat-v7/25.4.0/appcompat-v7-25.4.0.pom')
# download(r'http://www.cnblogs.com/paomaliuju/p/5176461.html')