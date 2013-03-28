# -*- coding: iso-8859-1 -*-
"""
    Zepheira MoinMoin 1.9.x wiki theme

    Based on the MoinMoin - modernized theme

    @copyright: 2003-2005 Nir Soffer, Thomas Waldmann
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase
from MoinMoin import wikiutil
from MoinMoin.Page import Page

class Theme(ThemeBase):

    name = "zepheira"

    _ = lambda x: x     # We don't have gettext at this moment, so we fake it
    icons = {
        # key         alt                        icon filename      w   h
        # FileAttach
        'attach':     ("%(attach_count)s",       "moin-attach.png",   16, 16),
        'info':       ("[INFO]",                 "moin-info.png",     16, 16),
        'attachimg':  (_("[ATTACH]"),            "attach.png",        32, 32),
        # RecentChanges
        'rss':        (_("[RSS]"),               "moin-rss.png",      16, 16),
        'deleted':    (_("[DELETED]"),           "moin-deleted.png",  16, 16),
        'updated':    (_("[UPDATED]"),           "moin-updated.png",  16, 16),
        'renamed':    (_("[RENAMED]"),           "moin-renamed.png",  16, 16),
        'conflict':   (_("[CONFLICT]"),          "moin-conflict.png", 16, 16),
        'new':        (_("[NEW]"),               "moin-new.png",      16, 16),
        'diffrc':     (_("[DIFF]"),              "moin-diff.png",     16, 16),
        # General
        'bottom':     (_("[BOTTOM]"),            "moin-bottom.png",   16, 16),
        'top':        (_("[TOP]"),               "moin-top.png",      16, 16),
        'www':        ("[WWW]",                  "moin-www.png",      16, 16),
        'mailto':     ("[MAILTO]",               "moin-email.png",    16, 16),
        'news':       ("[NEWS]",                 "moin-news.png",     16, 16),
        'telnet':     ("[TELNET]",               "moin-telnet.png",   16, 16),
        'ftp':        ("[FTP]",                  "moin-ftp.png",      16, 16),
        'file':       ("[FILE]",                 "moin-ftp.png",      16, 16),
        # search forms
        'searchbutton': ("[?]",                  "moin-search.png",   16, 16),
        'interwiki':  ("[%(wikitag)s]",          "moin-inter.png",    16, 16),
    }
    del _
    def header(self, d, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            u'<div id="mastwrap"><div id="masthead">',
            self.logo(),
            self.searchform(d),
            self.username(d),
            u'</div></div>',
            # self.navibar(d),
            self.trail(d),
            self.extranav(d),
            self.editbar(d),
            u'<div id="pageline"><hr style="display:none;"></div>',
            u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),
            self.msg(d),

            u'<h1 id="locationline">',
            self.interwiki(d),
            self.title_with_separators(d),
            u'</h1>',

            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            u'<h1 id="locationline">',
            self.title_with_separators(d),
            u'</h1>',
            self.msg(d),
            u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def html_head(self, d):
        return ThemeBase.html_head(self, d) + '\n' + self.faviconLink()

    def faviconLink(self):
        prefix = self.cfg.url_prefix_static + '/'
        name = self.name
        return '<link rel="shortcut icon" href="%s%s/img/favicon.ico">\n' % (prefix, name)

    def footer(self, d, **keywords):
        """ Assemble wiki footer

        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']
        html = [
            # End of page
            #self.pageinfo(page),
            self.endPage(),

            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),

            # Footer
            u'<div id="footer">',
            self.editbar(d),
            self.footerlinks(),
            #self.credits(d),
            #self.showversion(d, **keywords),
            u'</div>',

            ]
        return u'\n'.join(html)

    def extranav(self, d):
        """ Assemble the helpful extra navigation

        Of course in a normal theme these come from wikiconfig.py 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: extranav html
        """
        request = self.request
        _ = request.getText
        changesPage = wikiutil.getLocalizedPage(request, 'RecentChanges')
        findPage = wikiutil.getLocalizedPage(request, 'FindPage')
        helpPage = wikiutil.getLocalizedPage(request, 'HelpContents')
        
        extralinks = []
        # Set page to localized RC page
        title = changesPage.split_title(request)
        extralinks.append(changesPage.link_to(request, text=title))
        # Set page to localized find page
        title = findPage.split_title(request)
        extralinks.append(findPage.link_to(request, text=title))
        # Set page to localized help page
        title = helpPage.split_title(request)
        extralinks.append(helpPage.link_to(request, text=title))
            
        extralinks = [u'<li>%s</li>\n' % link for link in extralinks]
        html = u'<ul class="extranav">\n%s</ul>' % ''.join(extralinks)
        return html

    def trail(self, d):
        """ Assemble page trail

        @param d: parameter dictionary
        @rtype: unicode
        @return: trail html
        """
        request = self.request
        user = request.user
        html = ''
        if not user.valid or user.show_page_trail:
            trail = user.getTrail()
            if trail:
                items = []
                for pagename in trail:
                    try:
                        interwiki, page = wikiutil.split_interwiki(pagename)
                        if interwiki != request.cfg.interwikiname and interwiki != 'Self':
                            link = (self.request.formatter.interwikilink(True, interwiki, page) +
                                    self.shortenPagename(page) +
                                    self.request.formatter.interwikilink(False, interwiki, page))
                            items.append(link)
                            continue
                        else:
                            pagename = page

                    except ValueError:
                        pass
                    page = Page(request, pagename)
                    title = page.split_title()
                    title = self.shortenPagename(title)
                    link = page.link_to(request, title)
                    items.append(link)
                html = u'<div id="pagetrail">%s</div>' % u'<span class="sep"> &raquo; </span>'.join(items)
        return html

    def interwiki(self, d):
        """ Assemble the interwiki name display, linking to page_front_page

        @param d: parameter dictionary
        @rtype: string
        @return: interwiki html
        """
        if self.request.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or 'Self'
            link = page.link_to(self.request, text=text, rel='nofollow')
            html = u'<span id="interwiki">%s<span class="sep">: </span></span>' % link
        else:
            html = u''
        return html

    def footerlinks(self):
        """ Copyright notices and local links """
        html = u'''
    <ul id="credits">
      <li>Powered by <a href="http://moinmo.in/">MoinMoin</a></li>
      <li>%s</li>
    </li>
''' % self.emit_custom_html(self.cfg.page_footer2)
        return html

def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

