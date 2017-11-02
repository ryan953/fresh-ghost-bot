import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import datetime
import re

from matplotlib.ticker import FuncFormatter, MaxNLocator

def prepareGraphData(data, notAfter):
  newData = []

  stopOrdinal = stringToDate(notAfter).toordinal()

  for key in data:
    value = data[key]
    dateObj = stringToDate(value['date'])
    ordinal = dateObj.toordinal()
    if ordinal <= stopOrdinal:
      newData.append(dict(
        dateStr=value['date'],
        date=dateObj,
        ordinal=ordinal,
        count=value['count'],
        additions=value['additions'],
        removals=value['removals'],
      ))

  return sorted(newData, key=lambda k: k['ordinal'])

def stringToDate(str):
  dateParts = [int(s) for s in re.split('-', str)]
  date = datetime.date(*dateParts)
  return date

def renderGraph(filename, data):
  dateValues = []
  countValues = []
  addedValues = []
  removedValues = []

  def format_date(x, pos=None):
    return datetime.date.fromordinal(int(x)).strftime('%Y-%m')

  for value in data:
    dateValues.append(value['ordinal'])
    countValues.append(value['count'])
    if value['additions'] > 0:
      addedValues.append(value['additions'])
    else:
      addedValues.append(None)
    if value['removals'] > 0:
      removedValues.append(-1 * value['removals'])
    else:
      removedValues.append(None)

  fig, axCount = plt.subplots()
  axAdd = axCount.twinx()

  axCount.set_zorder(axAdd.get_zorder() + 1) # put ax in front of ax2
  axCount.patch.set_visible(False) # hide the 'canvas'

  axCount.plot(dateValues, countValues, 'b-')
  axCount.set_ylabel('Total Employees',
    color='blue')
  for tl in axCount.get_yticklabels():
    tl.set_color('b')
  axCount.grid(True)
  axCount.xaxis.set_major_formatter(FuncFormatter(format_date))

  addMarkerline, addStemlines, addBaseline = axAdd.stem(dateValues, addedValues, 'g:')
  rmMarkerline, rmStemlines, rmBaseline = axAdd.stem(dateValues, removedValues, 'r:')
  axAdd.set_ylabel('Delta', color='g')
  for tl in axAdd.get_yticklabels():
    tl.set_color('g')

  axAdd.set_xbound(data[0]['ordinal'], data[-1]['ordinal'])

  plt.setp(addMarkerline, 'markerfacecolor', 'g')
  plt.setp(rmMarkerline, 'markerfacecolor', 'r')
  plt.setp(addBaseline, 'color', 'black', 'linewidth', 1)
  plt.setp(rmBaseline, 'color', 'black', 'linewidth', 1)

  plt.savefig(filename)
