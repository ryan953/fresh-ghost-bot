from debug import *

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
