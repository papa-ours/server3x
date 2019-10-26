class Choice:
  def __init__(self, name):
    self._name = name
    self._isBlocked = False
    self._isPicked = False

  def block(self):
    self._isBlocked = True

  def unblock(self):
    self._isBlocked = False

  def pick(self):
    if self._isBlocked:
      raise ValueError('Blocked choice cannot be picked')
    self._isPicked = True

  def getName(self):
    return self._name

  def isBlocked(self):
    return self._isBlocked

  def isPicked(self):
    return self._isPicked

  def isAvailable(self):
    return not (self._isBlocked or self._isPicked)