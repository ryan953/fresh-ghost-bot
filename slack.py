import json
import urllib2

def postGhostToSlack(endpoint, name):
  data = json.dumps({
    'text': '%s is a FreshGhost' % (name,),
  })
  urllib2.urlopen(
    urllib2.Request(endpoint, data)
  )

def postGraphToSlack(endpoint, date, graphURL, summaryData):
  data = json.dumps({
    'channel': '@ryan',

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
  print(data)
  print(urllib2.urlopen(
    urllib2.Request(endpoint, data)
  ))
