from debug import *
import datetime

from BeautifulSoup import BeautifulSoup, SoupStrainer

class HTMLPage(object):
  def __init__(self, url, cacheDir):
    self.url = url
    self._cacheDir = cacheDir
    self.parseOnly = SoupStrainer('body')

  def __str__(self):
    return self.url

  def cachedFilename(self):
    date = datetime.date.today()
    dateStr = '%s-%s-%s' % (date.year, date.month, date.day, )

    return self._cacheDir + dateStr + '-' + '.html'

  def getHtml(self):
    try:
      return open(self.cachedFilename(), 'r')
    except IOError as e:
      print("({})".format(e))
      return ''

  def getDom(self):
    return BeautifulSoup(self.getHtml(), parseOnlyThese=self.parseOnly)

