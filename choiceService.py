from PyInquirer import prompt

class ChoiceService:
  def __init__(self, max):
    self._max = max
    self._numberOfChoices = 0
    self._numberOfBlocks = 0

  def validateInt(self, n):
    try:
      return int(n)
    except ValueError:
      return -1

  def validateNumberOfChoices(self, n):
    n = self.validateInt(n)
    return 'Number of choices must be 1 and ' + str(int(self._max)) \
      if not (n > 0 and n <= self._max) else True

  def validateNumberOfBlocks(self, n):
    n = self.validateInt(n)
    return 'Number of choices must be 0 and ' + str(self._numberOfChoices - 1) \
      if not (n >= 0 and n < self._numberOfChoices) else True

  def askNumberOfChoices(self):
    questions = [
      {
        'type': 'input',
        'name': 'n_choices',
        'message': 'Number of choices',
        'validate': self.validateNumberOfChoices
      }
    ]
    self._numberOfChoices = int(prompt(questions)['n_choices'])

  def askNumberOfBlocks(self):
    questions = [
      {
        'type': 'input',
        'name': 'n_blocks',
        'message': 'Number of blocks',
        'validate': self.validateNumberOfBlocks
      }
    ]
    self._numberOfBlocks = int(prompt(questions)['n_blocks'])

  def getNumberOfChoices(self):
    return self._numberOfChoices

  def getNumberOfBlocks(self):
    return self._numberOfBlocks

  def setNumberOfChoices(self, n):
    validation = self.validateNumberOfChoices(n)
    if type(validation) is str:
      return validation 
    self._numberOfChoices = n

  def setNumberOfBlocks(self, n):
    validation = self.validateNumberOfBlocks(n)
    if type(validation) is str:
      return validation 
    self._numberOfBlocks = n