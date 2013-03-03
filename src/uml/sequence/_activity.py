'''
Created on 02-03-2013

@author: Marcin
'''

class Activity:
    def __init__(self, parent, start, finish, level = 0):
        self.parent = parent
        self.start = start
        self.finish = finish
        self.level = level
    def length(self):
        return self.finish - self.start

    def printOut(self, canvas):
        canvas.ref(self.level * self.parent.parent.config.STEP_OFFSET,
                   self.start,
                   "activity%s" % self.length())

    def __str__(self):
        if self.level == 0: return repr([self.start, self.finish])
        return "[%s: %s, %s]" % (self.level, self.start, self.finish)
    def __repr__(self): return str(self)

    def __eq__(self, other): return self.start == other.start and self.finish == other.finish
    def __ne__(self, other): return not self.__eq__(other)
    def __lt__(self, other):
        if self.start == other.start: return self.finish < other.finish
        return self.start < other.start
    def __le__(self, other):
        if self.start == other.start: return self.finish <= other.finish
        return self.start <= other.start
    def __gt__(self, other):
        if self.start == other.start: return self.finish > other.finish
        return self.start > other.start
    def __ge__(self, other):
        if self.start == other.start: return self.finish >= other.finish
        return self.start >= other.start
