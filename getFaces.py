from BeautifulSoup import SoupStrainer
from Pages import HTMLPage, PageDownloader
from TeamPage import TeamPage2015

from debug import *

import argparse
import codecs
import datetime
import json
import sys
import time
import urllib2

DATE = datetime.date.today()
DATE_STR = '%s-%s-%s' % (DATE.year, DATE.month, DATE.day, )

class DataImporter(object):
    def scrape(self, args):
        try:
            settings = json.load(open(args.config))
        except IOError as e:
            print('No config file %s found' % (args.config,))
            sys.exit(1)

        PageDownloader.verbose = args.verbose

        print('Starting %s' % (DATE_STR,))

        page = TeamPage2015(teamUrl=settings['teamUrl'], cacheDir=settings['cacheDir'])
        page.updateCache()

        allNames = page.getPeopleNames()
        print('Found %s names (incl dogs)' % (len(allNames),))

        ghosts = self.collectGhosts(allNames)
        print('Found %s ghosts' % (len(ghosts),))

        for ghost in ghosts:
            print('%s is a FreshGhost' % (ghost,))
            if args.slack:
                self.postToSlack(ghost)

        if args.save:
            print('Saving new names list to %s' % (settings['listFile'],))
            self.save(allNames)

        print('Done')

    def collectGhosts(self, allNames):
        ghosts = []
        with codecs.open(settings['listFile'], 'r', 'utf-8') as f:
            for line in f:
                name = line.strip('\n')
                if name not in allNames:
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
        backupFile = './data/' + DATE_STR + '.lst'
        self.writeFile(backupFile, newNames)
        self.writeFile(settings['listFile'], newNames)

    def writeFile(self, filename, lines):
        with codecs.open(filename, 'w', 'utf-8') as f:
            f.write("\n".join(lines))
        f.closed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', action='store', help='read files from cacheDir', default='./config.json')
    parser.add_argument('--save', action='store_true', help='save new list')
    parser.add_argument('--slack', action='store_true', help='post to slack')
    parser.add_argument('--verbose', action='store_true', help='verbose output')

    importer = DataImporter()
    importer.scrape(parser.parse_args())
