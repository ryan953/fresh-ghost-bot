import json
import urllib2

def postSlackData(endpoint, data, channel):
  if channel:
    data['channel'] = channel

  print(json.dumps(data))
  urllib2.urlopen(urllib2.Request(endpoint, json.dumps(data)))

def postGhostsToSlack(endpoint, names, channel=None):
  postSlackData({
    'text': '\n'.join(['%s is a FreshGhost' % (name,) for name in names]),
  })

def postFreshiesToSlack(endpoint, names, channel=None):
  postSlackData({
    'text': '\n'.join(['%s is new\n' % (name,) for name in names]),
  })

def postGraphToSlack(endpoint, date, graphURL, summaryData, channel=None):
  postSlackData({
    'attachments': [{
      'fallback': 'Today\'s employee chart is ready',
      'title': 'Employee Growth Chart - %s' % (date, ),
      'text': 'Previous charts are available at <https://fresh-faces.ryan953.com/graphs/>.\nThe updated stats are:',
      'fields': [
        {'title': 'Additions', 'value': summaryData['additions'], 'short': True},
        {'title': 'Removals', 'value': summaryData['removals'], 'short': True},
        {'title': 'Total Employees', 'value': summaryData['count'], 'short': True},
      ],
      'image_url': graphURL,
    }]
  })
