class Node:
  def __init__(self, type, value = None, children = None):
    self.type = type
    self.value = value
    self.children = children

  def printSelf(self):
    print(self.type)
    print(self.value)
    print(self.children)