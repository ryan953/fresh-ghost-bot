from BeautifulSoup import BeautifulSoup, SoupStrainer

from debug import *

class HTMLPage(object):
  def __init__(self, filename):
    self.filename = filename
    self.parseOnly = SoupStrainer('body')

  def getHtml(self):
    try:
      return open(self.filename, 'r')
    except IOError as e:
      print("({})".format(e))
      return ''

  def getDom(self):
    return BeautifulSoup(self.getHtml(), parseOnlyThese=self.parseOnly)

  def getPeopleNames(self):
    # Override in subclasses
    pass

class TeamPage2015(HTMLPage):
    def __init__(self, teamUrl, cacheDir):
        super(TeamPage2015, self).__init__(teamUrl, cacheDir)

    def getPeopleNames(self):
        soup = self.getDom()
        titles = soup.findAll('div', 'team-name-container') # need to find all `.team-name-container > h3`
        names = []
        for title in titles:
            names.append(title.find('h3').extract().text)
        return names
