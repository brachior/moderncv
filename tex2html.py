__author__ = 'brachior'

import os as _os
from texparser.parser import TeXFactory as _TeXFactory
from texparser.parser import TeXParser as _TeXParser


class ModernCV(_TeXParser):
    def __init__(self, filename):
        self.filename = filename
        factory = _TeXFactory()
        style = ModernCVStyle()
        factory.add('macro', 'moderncvstyle', argc=1, store=style.set_style)
        factory.add('macro', 'moderncvcolor', argc=1, store=style.set_color)
        head = ModernCVHead()
        factory.add('macro', 'name', argc=2, store=head.set_name)
        factory.add('macro', 'phone', argc=1, store=head.set_phone)
        factory.add('macro', 'address', argc=1, argo=2, store=head.set_address)
        factory.add('macro', 'email', argc=1, store=head.set_email)
        factory.add('macro', 'homepage', argc=1, store=head.set_homepage)
        factory.add('macro', 'social', argc=1, store=head.set_social)
        factory.add('macro', 'extrainfo', argc=1, store=head.set_extra)
        factory.add('macro', 'photo', argc=1, store=head.set_photo)
        content = ModernCVContent()
        factory.add('macro', 'section', argc=1, store=content.set_section)
        factory.add('macro', 'subsection', argc=1, store=content.set_subsection)
        factory.add('macro', 'cventry', argc=6, store=content.set_cventry)
        factory.add('macro', 'cvitem', argc=2, store=content.set_cvitem)
        factory.add('macro', 'cvitemwithcomment', argc=2, argo=1,
                    store=content.set_cvlanguage)
        factory.add('macro', 'cvlanguage', argc=2, argo=1,
                    store=content.set_cvlanguage)
        factory.add('macro', 'cvdoubleitem', argc=4,
                    store=content.set_cvcomputer)
        factory.add('macro', 'cvcomputer', argc=4, store=content.set_cvcomputer)
        factory.add('macro', 'cvlistitem', argc=1, store=content.set_cvlistitem)
        factory.add('macro', 'cvlistdoubleitem', argc=2,
                    store=content.set_cvlistdoubleitem)
        self.style = style
        self.head = head
        self.content = content
        super().__init__(filename, factory)

    def __str__(self):
        return '''
<!DOCTYPE html>
<html>
    %s
    <body>
        <div class="moderncv" style="width: 800px; background-color: #fafafa">
            %s
            %s
        </div>
    </body>
</html>''' % (self.style, self.head, self.content)


class ModernCVStyle(object):
    def __init__(self):
        self.style = 'classic'
        self.color = 'blue'

    def set_style(self, attr, args):
        self.style = args[0]

    def set_color(self, attr, args):
        self.color = args[0]

    def __str__(self):
        return '''
    <head lang="en">
        <meta charset="UTF-8">
        <title></title>
        <link type="text/css" rel="stylesheet" href="moderncv/%s-%s.min.css"/>
    </head>
        ''' % (self.style, self.color)


class ModernCVHead(object):
    socials = {
        'bitbucket': 'https://bitbucket.org/',
        'github': 'https://github.com/jdoe',
        'git': '',
        'linkedin': 'http://www.linkedin.com/in/',
        'twitter': 'http://www.twitter.com/'
    }

    def __init__(self):
        self.name = ''
        self.phone = []
        self.address = ''
        self.email = ''
        self.homepage = ''
        self.social = []
        self.extra = ''
        self.photo = ''

    def set_name(self, attr, args):
        self.name = '<span class="mcv-name">\n%s\n</span>' \
                    % '\n'.join('<span>%s</span>' % s for s in args)

    def set_phone(self, attr, args):
        self.phone.append('<span class="icon icon-phone-%s">%s</span>'
                          % ((attr and str(attr) or 'mobile'), str(args[0])))

    def set_address(self, attr, args):
        self.address = '<span class="mcv-address">\n%s\n</span>' \
                       % '\n'.join('<span>%s</span>' % s for s in args)

    def set_email(self, attr, args):
        self.email = '<span class="icon icon-email"><a href="mailto:%s">%s</a></span>' \
                     % (args[0], args[0])

    def set_homepage(self, attr, args):
        self.homepage = '<span class="icon icon-homepage"><a href="%s">%s</a></span>' \
                        % (args[0], args[0])

    def set_social(self, attr, args):
        self.social.append(
            '<span class="icon icon-social-%s"><a href="%s%s">%s</a></span>'
            % (attr[0], ModernCVHead.socials[attr[0]], args[0], args[0]))

    def set_extra(self, attr, args):
        self.extra = '<span>%s</span>' % args[0]

    def set_photo(self, attr, args):
        exts = ['.png', '.jpg', '.gif', '.jpeg']
        pic = args[0]
        dirname = _os.path.dirname(pic)
        dirname = dirname and dirname or './'
        for f in (x for x in _os.listdir(dirname) if
                  _os.path.isfile(x) and x.startswith(pic) and x.find(
                      '.') != -1):
            name = f.lower()
            ext = name[name.rfind('.'):]
            if ext in exts:
                pic = dirname + f
                break
        else:
            self.photo = ''
        self.photo = '<img src="%s" alt="photo"/>' % pic

    def __str__(self):
        return '''
            <span class="mcv-head">
                <span class="mcv-info">
                    %s
                    <span class="mcv-contact">
                        %s
                        %s
                        %s
                        %s
                        %s
                        %s
                    </span>
                </span>
                %s
            </span>
        ''' % (self.photo, self.address, '\n'.join(self.phone), self.email,
               self.homepage, '\n'.join(self.social), self.extra, self.name)


class ModernCVContent(object):
    def __init__(self):
        self.content = ''

    def set_cventry(self, attr, args):
        """
        \cventry{year--year}{Degree}{Institution}{City}{\textit{Grade}}{Description}
        """
        self.content += '''<span class="mcv-cventry">
    <span>{0}</span>
    <span>
        <span>{1}</span>
        <span>{2}</span>
        <span>{3}</span>
        <span>{4}</span>
        <span>{5}</span>
    </span>
</span>\n'''.format(*args)

    def set_cvitem(self, attr, args):
        """
        \cvitem{hobby 1}{Description}
        """
        self.content += '''<span class="mcv-cvitem">
    <span>{0}</span>
    <span>{1}</span>
</span>
\n'''.format(*args)

    def set_cvlanguage(self, attr, args):
        """
        \cvlanguage{Language 1}{Skill level}{Comment}
        \cvitemwithcomment{Language 1}{Skill level}{Comment}
        """
        self.content += '''<span class="mcv-cvlanguage">
    <span>%s</span>
    <span>%s</span>
    %s
</span>\n''' % (args[0], args[1],
                len(args) == 3 and '<span>%s</span>' % args[2] or '')

    def set_cvcomputer(self, attr, args):
        """
        \cvcomputer{category 1}{XXX, YYY, ZZZ}{category 4}{XXX, YYY, ZZZ}
        \cvdoubleitem{category 1}{XXX, YYY, ZZZ}{category 4}{XXX, YYY, ZZZ}
        """
        self.content += '''<span class="mcv-cvcomputer">
    <span>
        <span>%s</span>
        <span>%s</span>
    </span>
    <span>
        <span>%s</span>
        <span>%s</span>
    </span>
</span>\n''' % (args[2], args[3], args[0], args[1])

    def set_cvlistitem(self, attr, args):
        """
        \cvlistitem{Item 1}
        """
        self.content += '''
<span class="mcv-listitem"><span>%s</span></span>\n''' % args[0]

    def set_cvlistdoubleitem(self, attr, args):
        """
        \cvlistdoubleitem{Item 1}{Item 4}
        """
        self.content += '''<span class="mcv-listdoubleitem">
    <span><span><span>%s</span></span></span>
    <span><span>%s</span></span>
</span>\n''' % (args[1], args[0])

    def set_section(self, attr, args):
        """
        \section{Education}
        """
        self.content += '<span class="mcv-section">%s</span>\n' % str(args[0])

    def set_subsection(self, attr, args):
        """
        \subsection{Vocational}
        """
        self.content += '<span class="mcv-subsection">%s</span>\n' % str(
            args[0])

    def __str__(self):
        return self.content


if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2:
        print("'tex2html.py' needs the tex file to convert")
    else:
        moderncv = ModernCV(argv[1])
        moderncv.parse()
        print(moderncv)
