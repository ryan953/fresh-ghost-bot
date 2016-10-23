from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString

from debug import *

def getFromTeamNameContainer(soup):
  titles = soup.findAll('div', 'team-name-container') # need to find all `.team-name-container > h3`
  return [title.find('h3').string for title in titles]

def getH3FromTeamImg(soup):
  images = soup.findAll('img', 'teamImg') # need to find all `img[class=teamImg] & h3`
  return [img.findNextSibling('h3').string for img in images]

def getH3UnderTeamClass(soup):
  titles = soup.findAll('div', 'team') # need to find all `.team > h3`
  return [title.find('h3').string for title in titles]

def getPreDashNames(soup):
  exec_cards = soup.findAll('div', 'exec') # need to find all `.exec > .name`
  execs = [card.find('span', 'name').string for card in exec_cards]
  empl_cards = soup.findAll('div', 'freshbooker') # need to find all `.freshbooker > .name`
  freshbookers = [card.find('span', 'name').string for card in empl_cards]
  return execs + freshbookers

def getDashNames(soup):
  execs = soup.findAll('h3', 'exec-name')
  freshbookers = soup.findAll('h3', 'freshbooker-name')
  return execs + freshbookers

class HTMLPage(object):
  def __init__(self, filename):
    self.filename = filename
    self.parseOnly = SoupStrainer('body')

  def getHtml(self):
    return open(self.filename, 'r')

  def getDom(self):
    return BeautifulSoup(
      self.getHtml(),
      parseOnlyThese=self.parseOnly,
      convertEntities=BeautifulSoup.HTML_ENTITIES
    )

  def getPeopleNames(self):
    soup = self.getDom()

    strategies = [
      getFromTeamNameContainer,
      getH3FromTeamImg,
      getH3UnderTeamClass,
      getPreDashNames,
      getDashNames,
    ]

    for strat in strategies:
      names = strat(soup)
      if len(names) > 0:
        print('Parsing HTML with %s - found names' % (strat.func_name, ))
        return names
      else:
        print('Parsing HTML with %s - no names' % (strat.func_name, ))

    return None
