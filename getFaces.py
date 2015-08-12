from BeautifulSoup import SoupStrainer
from Pages import HTMLPage

from debug import *

import argparse
import codecs
import json
import time
import urllib2

settings = {
    'debugging':True,
    'logging':True,
    'errors':True,
    'cacheDir':'./data/',
    'teamUrl': 'http://www.freshbooks.com/our-team.php',
    'listFile': './data/last-run.lst',
    'slack': {
        'endpoint': 'https://hooks.slack.com/services/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',
    }
}

class TeamPage(HTMLPage):
    def __init__(self, teamUrl, cacheDir):
        super(TeamPage, self).__init__(teamUrl, cacheDir)

    def getPeopleNames(self):
        soup = self.getDom()
        titles = soup.findAll('div', 'team-name-container') # need to find all `.team-name-container > h3`
        names = []
        for title in titles:
            names.append(title.find('h3').extract().text)
        return names

class DataImporter(object):
    def scrape(self, args):
        page = TeamPage(teamUrl=settings['teamUrl'], cacheDir=settings['cacheDir'])
        page.updateCache()

        newNames = page.getPeopleNames()

        ghosts = self.collectGhosts(newNames)
        for ghost in ghosts:
            print('%s is a FreshGhost' % (ghost,))
            if args.slack:
                self.postToSlack(ghost)

        if args.save:
            print 'Saving new names list'
            self.save(newNames)

    def collectGhosts(self, newNames):
        ghosts = []
        with codecs.open(settings['listFile'], 'r', 'utf-8') as f:
            for line in f:
                name = line.strip('\n')
                if name not in newNames:
                    ghosts.append(name)
        f.closed
        return ghosts

    def postToSlack(self, name):
        data = json.dumps({
            'text': '%s is a FreshGhost' % (name,),
        })
        urllib2.urlopen(
            urllib2.Request(settings['slack']['endpoint'], data)
        )
        print('Posted to slack about %s', (name,))

    def save(self, newNames):
        with codecs.open(settings['listFile'], 'w', 'utf-8') as f:
            f.write("\n".join(newNames))
        f.closed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action='store_true', help='save new list')
    parser.add_argument('--slack', action='store_true', help='post to slack')

    importer = DataImporter()
    importer.scrape(parser.parse_args())
