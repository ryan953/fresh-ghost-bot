from utils import getMissingNames

def test_getMissingNames():
  oldList = ['Alice', 'Bob', 'Carol']
  newList = ['Alice', 'Carol']
  missing = getMissingNames(oldList, newList)
  assert missing == ['Bob']
