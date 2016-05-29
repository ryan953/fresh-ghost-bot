import datetime
import matplotlib.pyplot as plt
import re

from matplotlib.ticker import FuncFormatter, MaxNLocator

def prepareGraphData(data, notAfter):
  newData = []

  stopOrdinal = stringToDate(notAfter).toordinal()

  for key in data:
    value = data[key]
    ordinal = stringToDate(value['date']).toordinal()
    if ordinal <= stopOrdinal:
      newData.append(dict(
        date=value['date'],
        ordinal=ordinal,
        count=value['count'],
        additions=value['additions'],
        removals=-1 * value['removals'],
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

  for value in data:
    dateValues.append(value['ordinal'])
    countValues.append(value['count'])
    addedValues.append(value['additions'])
    removedValues.append(value['removals'])

  fig, axCount = plt.subplots()
  axAdd = axCount.twinx()

  axCount.plot_date(dateValues, countValues, 'b-',
    xdate=True, ydate=False)
  axCount.set_ylabel('Total Employees',
    color='blue')
  for tl in axCount.get_yticklabels():
    tl.set_color('b')
  axCount.grid(True)
  # axCount.set_zorder(2)

  axAdd.plot_date(
    dateValues, addedValues, 'g-')
  axAdd.plot_date(
    dateValues, removedValues, 'r-')
  axAdd.set_ylabel('Delta',
    color='g')
  for tl in axAdd.get_yticklabels():
    tl.set_color('g')
  # axAdd.set_zorder(1)

  axAdd.set_xbound(data[0]['ordinal'], data[-1]['ordinal'])

  plt.savefig(filename)
