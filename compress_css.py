__author__ = 'brachior'

import os as _os
from csscompressor import compress as _compress
import re as _re

re_import = _re.compile("@import ['\"](?P<file>[^'\"]+)['\"]")


def extends_css(css_file):
    dir = _os.path.dirname(css_file) + '/'
    with open(css_file) as f:
        css = ''
        for line in f.readlines():
            if line.startswith('@import'):
                css += extends_css(dir + re_import.match(line).group('file'))
            else:
                css += line
    return css


def compress_css(css_file):
    css = extends_css(css_file)
    with open(css_file.replace('.css', '.min.css'), 'w+') as f:
        f.write(_compress(css))


if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2:
        print("'compress_css.py' needs the css file to compress")
    else:
        compress_css(argv[1])
