'''
Created on 02-03-2013

@author: Marcin
'''

def xmlize(s): return s

def def_object(config):
    return '''    <rect
      xml:id="object"
      x="0" y="0" width="%s" height="%s"
      />
''' % (config.OBJECT_WIDTH, config.OBJECT_HEIGHT)

def def_lifeline(config, length, suffix = ""):
    return '''    <line
      xml:id="lifeline%s"
      class="lifeline"
      x1="%.1f" y1="%s" x2="%.1f" y2="%s"
      />
''' % (suffix, float(config.OBJECT_WIDTH)/2, config.OBJECT_HEIGHT, float(config.OBJECT_WIDTH)/2, config.OBJECT_HEIGHT/2 + length)

def def_activity(config, length):
    return '''    <rect
      xml:id="activity%s"
      x="%.1f" y="%s" width="%s" height="%s"
      />
''' % (length, float(config.OBJECT_WIDTH)/2 - float(config.STEP_WIDTH)/2, config.OBJECT_HEIGHT/2, config.STEP_WIDTH, length)

def def_destroy(config):
    return '''      <g
      xml:id="destroy"
      class="destroy"
      transform="translate(%.1f,%s)">
      <line x1="-10" y1="-10" x2="10" y2="10" />
      <line x1="10" y1="-10" x2="-10" y2="10" />
    </g>
''' % (float(config.OBJECT_WIDTH)/2, config.OBJECT_HEIGHT/2)

DOC_START = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="%.4fin" height="%.4fin" viewBox="0 0 %s %s">
  <title>SVG Drawing</title>
  <style type="text/css">
    text {
      font-family: sans-serif;
      font-size: 8pt;
      stroke: none;
      fill: #333;
      text-anchor: middle
    }
    text.object {
      text-decoration: underline
    }
    rect {
      stroke: black;
      stroke-linecap: butt;
      fill: #ffa
    }
    .signal, .line {
      stroke: black;
      stroke-linecap: butt;
      fill: none
    }
    .block {
      stroke: black;
      stroke-linecap: butt;
      fill: black
    }
    .lifeline, .return {
      stroke: black;
      stroke-dasharray: 5 5
    }
    .destroy {
      stroke: black;
      stroke-width: 2;
      stroke-linecap: butt;
      fill: none
    }
  </style>
  <defs>
%s    <polyline
      xml:id="signalArrow"
      class="block"
      points="-10,-3 0,0 -10,3"
      />
    <polyline
      xml:id="asyncSignalArrow"
      class="line"
      points="-10,-3 0,0 -10,3"
      />
    <g
      xml:id="signal"
      class="signal"
      transform="translate(42.5, 50.71)">
      <line x1="0" y1="0" x2="113" y2="0" />
      <use xlink:href="#signalArrow" transform="translate(113)" />
    </g>
    <g
      xml:id="selfSignal"
      class="signal"
      transform="translate(42.5, 50.71)">
      <polyline class="line" points="0,0 62.5,0 62.5,25 0,25" />
      <use xlink:href="#syncSignalArrow" transform="translate(0, 25) scale(-1, 1)" />
    </g>
  </defs>'''

DOC_END = '</svg>'
