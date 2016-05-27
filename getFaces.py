from BeautifulSoup import SoupStrainer
from Downloader import Downloader
from Pages import HTMLPage, TeamPage2015

from debug import *
from files import readLines, writeLines, writeData
from slack import postToSlack
from utils import getFilenameForToday, getMissingNames

import argparse
import json
import sys

class DataImporter(object):
  def __init__(self, args):
    try:
      self.args = args
      self.settings = json.load(open(args.config))
    except IOError as e:
      print('No config file %s found' % (args.config,))
      sys.exit(1)

  def scrape(self):
    htmlFile = getFilenameForToday(self.settings['cacheDir'], '.html')
    print('Starting %s' % (htmlFile,))

    if (self.args.download):
      writeData(
        Downloader()
          .download(self.settings['teamUrl'], self.args.verbose),
        htmlFile
      )

    oldNameList = readLines(self.settings['listFile'])
    print('Found %s names from last time' % (len(oldNameList), ))

    newNameList = TeamPage2015(htmlFile).getPeopleNames()
    print('Found %s new names (incl dogs)' % (len(newNameList), ))

    ghosts = getMissingNames(oldNameList, newNameList)
    print('Found %s ghosts' % (len(ghosts), ))

    additions = len(newNameList) - len(oldNameList) - len(ghosts)
    print('Found %s new Freshies' % (additions, ))

    for ghost in ghosts:
      print('%s is a FreshGhost' % (ghost,))
      if self.args.postToSlack:
        postToSlack(self.settings['slack']['endpoint'], ghost)
        print('Posted to slack about %s', (name,))

    if self.args.save:
      print('Saving new names list to %s' % (self.settings['listFile'],))
      writeLines(getFilenameForToday(self.settings['cacheDir'], '.lst'), newNameList)
      writeLines(self.settings['listFile'], newNameList)

    print('Done')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', action='store', help='read files from cacheDir', default='./config.json')
  parser.add_argument('--save', action='store_true', help='save new list')
  parser.add_argument('--download', action='store_true', help='download todays file')
  parser.add_argument('--slack', action='store_true', help='post to slack')
  parser.add_argument('--verbose', action='store_true', help='verbose output')

  importer = DataImporter(parser.parse_args())
  importer.scrape()
