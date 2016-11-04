import json
import urllib2

def postSlackData(endpoint, channel, data):
  if channel:
    data['channel'] = channel

  print(json.dumps(data))
  urllib2.urlopen(urllib2.Request(endpoint, json.dumps(data)))

def postFacesToSlack(endpoint, date, freshies, ghosts, channel=None):
  postSlackData(endpoint, channel, {
    'attachments': [{
      'fallback': 'There are %s ghosts and %s freshies today!' % (len(ghosts), len(freshies), ),
      'title': 'Employee Changes - %s' % (date, ),
      'fields': [
        {'title': 'Ghosts', 'short': True, 'value': '\n'.join(ghosts)},
        {'title': 'Newbies', 'short': True, 'value': '\n'.join(freshies)},
      ],
    }],
  })

def postGraphToSlack(endpoint, date, graphURL, summaryData, channel=None):
  postSlackData(endpoint, channel, {
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
    }],
  })
