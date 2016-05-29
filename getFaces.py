from BeautifulSoup import SoupStrainer
from Downloader import Downloader
from Pages import HTMLPage

from debug import *
from files import readLines, writeLines, writeData, listFiles
from slack import postToSlack
from utils import getToday, getMissingNames, getFilenameBefore

import argparse
import json
import re
import sys

class DataImporter(object):
  def __init__(self, args):
    try:
      self.args = args
      local = open(args.config)
      self.settings = json.load(local)
      local.close()
    except IOError as e:
      print('No config file %s found' % (args.config,))
      sys.exit(1)

  def scrape(self):
    today = getToday()
    if self.args.date:
      today = self.args.date

    htmlFile = self.settings['cacheDir'] + today + '.html'
    listFile = self.settings['cacheDir'] + today + '.lst'

    print('Starting %s' % (htmlFile, ))
    print('List file %s' % (listFile, ))

    if (self.args.download):
      writeData(
        Downloader().download(self.settings['teamUrl'], self.args.verbose),
        htmlFile
      )

    allFiles = listFiles(self.settings['cacheDir'])
    prevListFile = getFilenameBefore(
      [f for f in allFiles if f[-4:] == '.lst'],
      listFile
    )

    newNameList = HTMLPage(htmlFile).getPeopleNames()
    print('Found %s new names (incl dogs)' % (len(newNameList), ))

    if prevListFile:
      oldNameList = readLines(prevListFile)
      print('Prev name list %s (%s names)' % (prevListFile, len(oldNameList), ))

      ghosts = getMissingNames(oldNameList, newNameList)
      print('Found %s ghosts' % (len(ghosts), ))

      remaining = len(oldNameList) - len(ghosts)
      additions = len(newNameList) - remaining
      print('Found %s new Freshies' % (additions, ))

      for ghost in ghosts:
        if self.args.verbose:
          print('%s is a FreshGhost' % (ghost, ))
        if self.args.slack:
          postToSlack(self.settings['slack']['endpoint'], ghost)
          print('Posted to slack about %s', (name, ))
    else:
      print('No prev name list found. Is this the start of time?')
      ghosts = []
      additions = 0

    if self.args.save:
      print('Saving new names list to %s' % (listFile, ))
      writeLines(listFile, newNameList)

      jsonFileReader = open(self.settings['jsonFile'], 'r')
      summaryData = json.load(jsonFileReader)
      summaryData[today] = dict(
        date=re.sub(r'(\d{4}\-\d{2}\-\d{2}).*', r'\1', today),
        count=len(newNameList),
        additions=additions,
        removals=len(ghosts),
      )
      jsonFileReader.close()

      print('Adding to summary json %s' % (self.settings['jsonFile'], ))
      jsonFileWriter = open(self.settings['jsonFile'], 'w')
      json.dump(summaryData, jsonFileWriter)
      jsonFileWriter.close()

    print('Done')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', action='store', help='read files from cacheDir', default='./config.json')
  parser.add_argument('--download', action='store_true', help='download todays file')
  parser.add_argument('--date', action='store', help='Use this date string for processing')
  parser.add_argument('--save', action='store_true', help='save new list & update summary json')
  parser.add_argument('--slack', action='store_true', help='post to slack')
  parser.add_argument('--verbose', action='store_true', help='verbose output')

  importer = DataImporter(parser.parse_args())
  importer.scrape()
