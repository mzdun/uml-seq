# encoding: utf-8

'''
Created on 02-03-2013

@author: Marcin
'''
import _activity
from _utils import xmlize

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

    def object_label(self, offY = 0):
        return '      <text class="object" transform="translate(%.1f,%s)">%s</text>' % \
            (float(self._config().OBJECT_WIDTH)/2, offY + self._config().OBJECT_HEIGHT - 12, xmlize(self.name))

    def printOut(self):
        if self.constructed_on == -1: return

        lifeline_suffix = ""
        if self.constructed_on != 0 or self.destroyed_on != -1:
            length = self.destroyed_on
            if length == -1: length = self.parent.now()
            length -= self.constructed_on
            lifeline_suffix = str(length)

        translate = ""
        start = self.constructed_on
        if self.index != 0 or self.constructed_on > 0:
            if self.index == 0:
                translate = "0"
            else:
                translate = "%s" % (self.index * self._config().OBJECT_DISTANCE)
            if self.constructed_on > 0:
                translate = "%s, %s" % (translate, start)
        if translate == "":
            print '    <g>'
        else:
            print '    <g transform="translate(%s)">' % translate

        print '      <use xlink:href="#lifeline%s"/>' % lifeline_suffix
        print '      <use xlink:href="#object"/>'
        print self.object_label();

        while len(self.activity_stack) > 0: self.inactive()
        activity = sorted(self.activity)
        for a in activity:
            a.printOut()
        if self.destroyed_on != -1:
            print '      <use xlink:href="#destroy" transform="translate(0, %s)"/>' % \
                (self.destroyed_on - self.constructed_on)

        print '    </g>'

    def printOutMessages(self):
        print '    <g transform="translate(%.1f)">' % \
            (float(self._config().OBJECT_WIDTH)/2 + self.index * self._config().OBJECT_DISTANCE)

        for msg in self.messages:
            msg.printOut()
        print '    </g>'
