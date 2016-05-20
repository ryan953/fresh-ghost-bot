from Pages import HTMLPage

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
