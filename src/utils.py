import datetime

def getToday():
  date = datetime.date.today()
  dateStr = '{:%Y-%m-%d}'.format(date)
  return dateStr

def getFilenameBefore(files, target):
  lessFiles = filter(lambda file: file < target, files)
  if len(lessFiles):
    return lessFiles[-1]
  else:
    return None

def getMissingNames(oldNameList, newNameList):
  ghosts = []
  for oldName in oldNameList:
    if oldName not in newNameList:
      ghosts.append(oldName)
  return ghosts
