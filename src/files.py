from debug import *
from os import listdir
from os.path import isfile, join

import codecs

def readLines(filename):
  lines = []
  with codecs.open(filename, 'r', 'utf-8') as f:
    for line in f:
      lines.append(line.strip('\n'))
  return lines

def writeLines(filename, lines):
  with codecs.open(filename, 'w', 'utf-8') as f:
    f.write("\n".join(lines))
  f.closed

def writeData(data, filename):
  local = open(filename, 'w')
  local.write(data)
  local.close()
  print('Saved To: %s' % (filename, ))

def listFiles(dir):
  onlyfiles = [dir + f for f in listdir(dir) if isfile(join(dir, f))]
  return sorted(onlyfiles)
