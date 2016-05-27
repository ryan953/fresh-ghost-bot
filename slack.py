import json
import urllib2

def postToSlack(endpoint, name):
  data = json.dumps({
    'text': '%s is a FreshGhost' % (name,),
  })
  urllib2.urlopen(
    urllib2.Request(endpoint, data)
  )
