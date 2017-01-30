import json
import urllib2

def postSlackData(endpoint, channel, data):
  if channel:
    data['channel'] = channel

  print(json.dumps(data))
  urllib2.urlopen(urllib2.Request(endpoint, json.dumps(data)))

def postFacesToSlack(endpoint, date, data, channel=None):
  postSlackData(endpoint, channel, {
    'attachments': [{
      'fallback': 'There are %s ghosts and %s freshies today.' % (len(data['removals']), len(data['additions']), ),
      'title': 'Employee Changes - %s' % (date, ),
      'text': 'Previous charts are available at <https://fresh-faces.ryan953.com/graphs/>.\nThe updated stats are:',
      'fields': [
        {'title': 'Ghosts', 'short': True, 'value': '\n'.join(data['removals'])},
        {'title': 'Newbies', 'short': True, 'value': '\n'.join(data['additions'])},
        {'title': 'Total Employees', 'value': data['count'], 'short': True},
      ],
      'image_url': data['graphURL'],
    }],
  })
