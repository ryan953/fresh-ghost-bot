from BeautifulSoup import BeautifulSoup, SoupStrainer

from debug import *

class HTMLPage(object):
  def __init__(self, filename):
    self.filename = filename
    self.parseOnly = SoupStrainer('body')

  def getHtml(self):
    return open(self.filename, 'r')

  def getDom(self):
    return BeautifulSoup(self.getHtml(), parseOnlyThese=self.parseOnly)

  def getPeopleNames(self):
    # Override in subclasses
    pass

class TeamPage2015(HTMLPage):
    def __init__(self, filename):
        super(TeamPage2015, self).__init__(filename)

    def getPeopleNames(self):
        soup = self.getDom()
        titles = soup.findAll('div', 'team-name-container') # need to find all `.team-name-container > h3`
        names = []
        for title in titles:
            names.append(title.find('h3').extract().text)
        return names
