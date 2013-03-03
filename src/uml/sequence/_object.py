# encoding: utf-8

'''
Created on 02-03-2013

@author: Marcin
'''
import _activity

class Object:
    def __init__(self, parent, index, name, alive):
        self.parent = parent
        self.index = index
        self.name = name
        if alive: self.constructed_on = 0
        else: self.constructed_on = -1
        self.destroyed_on = -1
        self.activity = []
        self.messages = []
        self.activity_stack = []

    def _config(self): return self.parent.config

    def active(self):
        self.activity_stack.append(self.parent.now())

    def inactive(self):
        level = len(self.activity_stack)
        if level == 0: return
        level -= 1
        start = self.activity_stack[level]
        finish = self.parent.now()
        if start == finish: return
        if self.constructed_on > 0:
            start -= self.constructed_on
            finish -= self.constructed_on
        self.activity_stack = self.activity_stack[:level]
        self.activity.append(_activity.Activity(self, start, finish, level))

    def sendTo(self, oth, name = None):
        self.messages.append(self.parent.addMessage(False, self, oth, name))

    def returnTo(self, oth, name = None):
        self.messages.append(self.parent.addMessage(True, self, oth, name))

    def create(self, oth):
        self.sendTo(oth, "«create»")
        oth.constructed_on = self.parent.now()
        self.parent.hstep();

    def destroy(self, oth):
        self.sendTo(oth, "«destroy»")
        oth.destroyed_on = self.parent.now()

    def level_at(self, timestamp):
        max_level = 0
        if self.constructed_on != -1:
            timestamp -= self.constructed_on
        for activity in self.activity:
            if activity.start <= timestamp and activity.finish >= timestamp:
                if max_level < activity.level:
                    max_level = activity.level
        return max_level

    def printOut(self, parent_canvas):
        if self.constructed_on == -1: return

        lifeline_suffix = ""
        if self.constructed_on != 0 or self.destroyed_on != -1:
            length = self.destroyed_on
            if length == -1: length = self.parent.now()
            length -= self.constructed_on
            lifeline_suffix = str(length)
        
        canvas = parent_canvas.canvas(self.index * self._config().OBJECT_DISTANCE,
                                      self.constructed_on)
        canvas.ref(0, 0, "lifeline%s" % lifeline_suffix)
        canvas.ref(0, 0, "object")

        canvas.text(float(self._config().OBJECT_WIDTH)/2, self._config().OBJECT_HEIGHT - 12, self.name, "object")

        while len(self.activity_stack) > 0: self.inactive()
        activity = sorted(self.activity)
        for a in activity:
            a.printOut(canvas)
        if self.destroyed_on != -1:
            canvas.ref(0, self.destroyed_on - self.constructed_on, "destroy")

    def printOutMessages(self, parent_canvas):
        canvas = parent_canvas.canvas(float(self._config().OBJECT_WIDTH)/2 + self.index * self._config().OBJECT_DISTANCE, 0)

        for msg in self.messages:
            msg.printOut(canvas)
