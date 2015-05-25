__author__ = 'brachior'


def _nothing(attr, args):
    pass


class TeXFactory(object):
    def __init__(self):
        self.macros = {}

    def add(self, kind, name, argc=0, argo=0, store=_nothing,
            render=lambda x, y: ''):
        if kind == 'macro':
            self.macros[name] = (name, argc, argo, store, render)

    def instance(self, kind, name):
        if kind == 'macro':
            return TeXMacro(*self.macros[name])

    def contains(self, kind, name):
        if kind == 'macro':
            return name in self.macros


class TeXMacro(object):
    def __init__(self, name, argc=0, argo=0, store=_nothing,
                 render=lambda x, y: ''):
        self.name, self.argc, self.argo = name, argc, argo * -1
        self.store, self.render = store, render
        self.attributes = []
        self.arguments = []

    def parse(self, block, i):
        self.attributes = []
        self.arguments = []
        stack_arg = []
        stack_attr = []
        nb_args = self.argc
        l = len(block)
        while i < l:
            c = block[i]
            if c == '{':
                stack_arg.append(i)
            elif c == '}' and stack_arg:
                start = stack_arg.pop()
                if len(stack_arg) == 0:
                    self.arguments.append(block[start + 1: i])
                    nb_args -= 1
            if c == '[':
                stack_attr.append(i)
            elif c == ']' and stack_attr:
                start = stack_attr.pop()
                if len(stack_attr) == 0:
                    self.attributes.append(block[start + 1: i])
            elif c == '\\':
                if self.argo <= nb_args <= 0:
                    self.store(self.attributes, self.arguments)
                    return i - 1
            i += 1

    def __str__(self):
        return self.render(self.attributes, self.arguments)


class TeXParser(object):
    def __init__(self, filename, factory):
        self.filename = filename
        self.factory = factory

    def parse(self):
        with open(self.filename) as f:
            self.parse_block(f.read())

    def parse_block(self, block):
        i = 0
        l = len(block)
        while i < l:
            c = block[i]
            if c == '%':
                while block[i] != '\n':
                    i += 1
            elif c == '\\':
                start = i
                i += 1
                while block[i] != '{' \
                        and block[i] != '[' \
                        and block[i] != '\\':
                    i += 1
                command = block[start + 1: i]
                if self.factory.contains('macro', command):
                    cmd = self.factory.instance('macro', command)
                    i = cmd.parse(block, i)
                    # fixme parse each arguments
                else:
                    # fixme environment
                    pass
                if block[i] == '\\':
                    i -= 1
            i += 1
