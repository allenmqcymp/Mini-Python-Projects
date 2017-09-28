# abstract model of the cell
# note to self: next time, no need to include setter and getter methods

class Cell(object):
    def __init__(self, id):
        self.isAlive = False
        self.id = id

    def getAlive(self):
        return self.isAlive

    def setAlive(self):
        self.isAlive = True

    def clearAlive(self):
        self.isAlive = False
