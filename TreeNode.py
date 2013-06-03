class TreeNode:
  """
    Simple binary tree structure that supports insert and lookup. Does not
    support delete and does not balance inserts in any way. To use, instance
    a node, set key and value attributes. For additional nodes, repeat
    steps for the root node to create a new child and call insert on the
    root passing the new child.
  """

  def __init__(self):
    self.lChild = 0
    self.rChild = 0
    self.key = 0
    self.value = 0

  def findValueByKey(self, key):
    if key == self.key:
      return self.value
    elif key > self.key and self.rChild != 0:
      return self.rChild.findValueByKey(key)
    elif key < self.key and self.lChild != 0:
      return self.lChild.findValueByKey(key)
    else:
      return 0    # not found

  def insert(self, newNode):
    if newNode.key == self.key:   # no duplicates allowed
      return    
    elif newNode.key > self.key:
      if self.rChild == 0:
        self.rChild = newNode
      else:
        self.rChild.insert(newNode)
    elif newNode.key < self.key:
      if self.lChild == 0:
        self.lChild = newNode
      else:
        self.lChild.insert(newNode)
