import datetime

def getFilenameForToday(folder, ext):
  date = datetime.date.today()
  dateStr = '{:%Y-%m-%d}'.format(date)
  return folder + dateStr + ext

def getFilenameBefore(files, target):
  lessFiles = filter(lambda file: file < target, files)
  return lessFiles[-1]

def getMissingNames(oldNameList, newNameList):
  ghosts = []
  for oldName in oldNameList:
    if oldName not in newNameList:
      ghosts.append(oldName)
  return ghosts
