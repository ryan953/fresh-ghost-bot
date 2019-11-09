import argparse
import json
import re
import sys

from Downloader import Downloader
from Pages import HTMLPage

from files import readLines, writeLines, writeData, listFiles
from graph import prepareGraphData, renderGraph
from slack import postFacesToSlack
from utils import getToday, getMissingNames, getFilenameBefore

class DataImporter(object):
  def __init__(self, args):
    try:
      self.args = args
      local = open(args.config)
      self.settings = json.load(local)
      local.close()
    except IOError as error:
      print 'No config file %s found (%s)' % (args.config, error)
      sys.exit(1)

  def scrape(self):
    today = getToday()
    if self.args.date:
      today = self.args.date
      self.args.download = False # can't set another date and download

    today_clean = re.sub(r'(\d{4}\-\d{2}\-\d{2}).*', r'\1', today)
    html_file = self.settings['cacheDir'] + today + '.html'
    list_file = self.settings['namesDir'] + today + '.lst'
    slack_channel = self.settings['slack'].get('channel', None)

    print 'Starting %s' % (today, )
    print 'HTML file %s' % (html_file, )
    print 'List file %s' % (list_file, )

    if self.args.download:
      writeData(
          Downloader().download(self.settings['teamUrl'], self.args.verbose),
          html_file)

    all_files = listFiles(self.settings['namesDir'])
    prev_list_file = getFilenameBefore(
        [f for f in all_files if f[-4:] == '.lst'],
        list_file)

    print 'Prev List file %s' % (prev_list_file, )

    new_name_list = HTMLPage(html_file).getPeopleNames()
    print 'Found %s new names' % (len(new_name_list), )

    if prev_list_file:
      old_name_list = readLines(prev_list_file)
      print 'Found %s prev names' % (len(old_name_list), )

      ghosts = getMissingNames(old_name_list, new_name_list)
      freshies = getMissingNames(new_name_list, old_name_list)
      print 'Found %s ghosts' % (len(ghosts), )
      print 'Found %s new Freshies' % (len(freshies), )

      if self.args.verbose:
        for name in ghosts:
          print '%s is a FreshGhost' % (name, )
        for name in freshies:
          print '%s is fresh' % (name, )

    else:
      print 'No prev name list found. Is this the start of time?'
      old_name_list = new_name_list
      ghosts = []
      freshies = new_name_list

    if self.args.save:
      print 'Saving new names list to %s' % (list_file, )
      writeLines(list_file, new_name_list)

      print 'Adding to summary json %s' % (self.settings['summaryFile'], )
      with open(self.settings['summaryFile'], 'r+') as summary_file:
        summary_data = json.load(summary_file)
        summary_data[today] = dict(
            date=today_clean,
            count=len(new_name_list),
            additions=len(freshies),
            removals=len(ghosts),
        )
        summary_file.seek(0)
        summary_file.truncate()
        json.dump(summary_data, summary_file, sort_keys=True)
        summary_file.close()

      print 'Adding to tenure json %s' % (self.settings['tenureFile'], )
      with open(self.settings['tenureFile'], "r+") as tenure_file:
        tenureSummary = json.load(tenure_file)
        tenureSummary[today_clean] = dict(
          date=today_clean,
          count=len(new_name_list),
          additions=len(freshies),
          removals=len(ghosts),
          survivors=old_name_list,
          newbies=freshies,
          ghosts=ghosts,
        )
        tenure_file.seek(0)
        tenure_file.truncate()
        json.dump(tenureSummary, tenure_file, sort_keys=True)
        tenure_file.close()

    if self.args.graph:
      print 'Building graph'
      json_file_reader = open(self.settings['summaryFile'], 'r')
      renderGraph(
          self.settings['graphDir'] + today_clean + '.png',
          prepareGraphData(json.load(json_file_reader), today_clean),
      )

    if self.args.slack:
        if self.args.graph:
            graphURL = self.settings['graphURLRoot'] + today_clean + '.png'
        else:
            graphURL = None

        postFacesToSlack(
            self.settings['slack']['endpoint'],
            today_clean,
            dict(
                graphURL=graphURL,
                count=len(new_name_list),
                additions=freshies,
                removals=ghosts,
            ),
            slack_channel)
        print 'Posted graph image to slack channel %s' % (slack_channel, )


    print 'Done'


if __name__ == "__main__":
  PARSER = argparse.ArgumentParser()
  PARSER.add_argument(
      '--config',
      action='store',
      help='read files from cacheDir',
      default='./config.json')
  PARSER.add_argument(
      '--date',
      action='store',
      help='Use this date string for processing')
  PARSER.add_argument('--download', action='store_true', help='download todays file')
  PARSER.add_argument(
      '--graph',
      action='store_true',
      help='create a graph with the summary data')
  PARSER.add_argument(
      '--save',
      action='store_true',
      help='save new list & update summary json')
  PARSER.add_argument('--slack', action='store_true', help='post to slack')
  PARSER.add_argument('--verbose', action='store_true', help='verbose output')
  PARSER.add_argument('--newbies', action='store_true', help='verbose output')

  IMPORTER = DataImporter(PARSER.parse_args())
  IMPORTER.scrape()
