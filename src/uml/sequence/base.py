'''
Created on 03-03-2013

@author: Marcin
'''
class Config:
    PAGE_MARGIN = 50
    OBJECT_DISTANCE = 125
    OBJECT_WIDTH = 75
    OBJECT_HEIGHT = 30
    STEP_WIDTH = 10
    STEP_HEIGHT = 25
    STEP_OFFSET = 5

class Diagram:
    def object(self, name): return None
    def pobject(self, name): return None

    def async(self): pass
    def sync(self): pass
    def step(self): pass

class Object:
    def active(self): pass
    def inactive(self): pass
    def sendTo(self, oth, name = None): return None
    def returnTo(self, oth, name = None): return None
    def create(self, oth): return None
    def destroy(self, oth): return None
