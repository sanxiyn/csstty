from __future__ import print_function

import html5lib
import cssutils
# A patched version of lxml.cssselect to handle a default namespace
import cssselect
import termcolor

XHTML_PREFIX = 'html'
XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'

class StyleRenderer(object):
    def __init__(self):
        super(StyleRenderer, self).__init__()
        self.stylesheets = []
        self.rules = []
    def load_style(self, style):
        stylesheet = cssutils.parseString(style)
        self.stylesheets.append(stylesheet)
        for rule in stylesheet:
            if rule.type == rule.STYLE_RULE:
                rule.selector = cssselect.CSSSelector(rule.selectorText,
                    namespaces={XHTML_PREFIX: XHTML_NAMESPACE})
                self.rules.append(rule)
    def render(self, htmlfile):
        f = open(htmlfile)
        self.tree = html5lib.parse(f, treebuilder='lxml')
        self.handle(self.tree.getroot())
    def handle(self, element):
        style = {}
        # TODO: cascade
        for rule in self.rules:
            if element in rule.selector(self.tree):
                for property in rule.style:
                    style[property.name] = property.value
        if style:
            self.start_element(element, style)
        for child in element:
            tag = child.tag
            if tag[:1] == '{':
                tag = tag.rsplit('}', 1)[1]
            method = getattr(self, 'handle_' + tag, None)
            if method:
                method(child)
            else:
                self.handle(child)
        if style:
            self.end_element(element, style)
    def handle_style(self, element):
        self.load_style(element.text)

class Renderer(StyleRenderer):
    def start_element(self, element, style):
        display = style.get('display')
        if not display:
            return
        if display == 'inline':
            print(element.text, end='')
            if element.tail:
                tail = element.tail.strip() or ' '
                print(tail, end='')
        elif display == 'block':
            print(element.text)
    def end_element(self, element, style):
        display = style.get('display')
        if not display:
            return
        if display == 'block':
            print()

DEFAULT_STYLESHEET = '''
p { display: block; }
'''

import sys
args = sys.argv[1:]
if len(args) != 1:
    print('Usage: csstty.py htmlfile')
    sys.exit()

htmlfile = args[0]

renderer = Renderer()
renderer.load_style(DEFAULT_STYLESHEET)
renderer.render(htmlfile)
