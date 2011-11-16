#!/usr/bin/env python
"""
------------------------------------
NiftyArticles v0.4, GTK version

Made by Florentin Sardan
florentinwww (at) gmail.com

Project's page:
    http://www.betterprogramming.com/niftyarticles-extract-articles-from-any-webpage-with-python-webkit-and-readability.html
My portfolio:
    http://www.betterprogramming.com/

Readability webpage:
    http://lab.arc90.com/experiments/readability/
------------------------------------
Install the required resources, python 2.6, python webkit bindings and python gtk2 bindings

Ubuntu or Debian
sudo apt-get install python2.6 python-webkit python-gtk2

Mark the script as executable
chmod +x niftyarticles-gtk.py

Usage Examples:
python niftyarticles-gtk.py --help

# save an article from ubuntu.com
python niftyarticles-gtk.py -u http://www.ubuntu.com/project/derivatives

# hide the browser window, don't load images, don't load java applets, save article to myarticle.txt from specified url 
python niftyarticles-gtk.py -b -i -j -f myarticle.txt -u http://www.ubuntu.com/project/canonical-and-ubuntu

Webkit Reference
http://webkitgtk.org/reference/index.html
"""

import sys
import gtk
import webkit
import os
import time
from optparse import OptionParser
import warnings
warnings.filterwarnings('ignore')

class GtkCrawler(gtk.Window):
    def __init__(self, options):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.move(0, 0)
        #self.resize(800,600)
        self.resize(gtk.gdk.screen_width()-200, gtk.gdk.screen_height()-200)
        self.options = options

    def run(self):
        webview = webkit.WebView()

        websettings = webview.get_settings()
        websettings.set_property("auto-load-images", self.options.images)
        websettings.set_property("enable-java-applet", self.options.java)
        websettings.set_property("enable-page-cache", True)
        websettings.set_property("enable-plugins", self.options.plugins)

        subwindow = gtk.ScrolledWindow()
        subwindow.add(webview)

        webview.load_uri(self.options.url)

        webview.connect('load-finished', self.load_finished)
        webview.connect('document-load-finished', self.document_load_finished)
        #webview.connect('load-progress-changed', self.load_progress_changed)
        webview.connect("console-message" , self.console_message)
        self.add(subwindow)
        
        if self.options.browser:
            self.show_all()
            
        self.connect('delete-event', lambda window, event: gtk.main_quit())
        gtk.main()
 
    def document_load_finished(self, webview, webframe):
        """ in case that page is not fully loaded, we set a timeout """
        script = """
function timeout() {
    clearTimeout(timeoutID);
    throw('<!-- timeout -->');
}
var timeoutID=setTimeout("timeout()", 5000);
        """
        webview.execute_script(script)
    
    def load_finished(self, webview, webframe):
        self.readability(webview)
    
    def readability(self, webview):
        if getattr(self, 'extracting', None): return True
        
        with open('readability.js', 'r') as f:
            readability_code = f.read()
        
        #readability_code = """(function(){readConvertLinksToFootnotes=false;readStyle='style-newspaper';readSize='size-medium';readMargin='margin-wide';_readability_script=document.createElement('script');_readability_script.type='text/javascript';_readability_script.src='http://lab.arc90.com/experiments/readability/js/readability.js?x='+(Math.random());document.documentElement.appendChild(_readability_script);})();"""
        script = """
readConvertLinksToFootnotes=false;readStyle='style-newspaper';readSize='size-medium';readMargin='margin-wide';
"""+readability_code+""";
function timedCount() {
    var readability_content = document.getElementById("readability-content");
    if (readability_content) {
        clearInterval(intervalID);
        var html = '<!-- article --><h1 class="supertitle">'+document.title + '</h1>' + readability_content.innerHTML;
        throw(html);
    }
}
var intervalID = setInterval("timedCount()", 100);
var timeoutID = setTimeout("throw('<!-- exit -->');", 5000); // exit after 5 seconds
        """
        setattr(self, 'extracting', True)
        webview.execute_script(script)

    def console_message(self, webview, msg, line, sourceid):
        content = msg
        if content.startswith('<!-- article -->'):
            print content
            self.bye()
        if content.startswith('<!-- exit -->'):
            print >> sys.stderr, 'exit'
            self.bye()
        if content.startswith('<!-- timeout -->'):
            print >> sys.stderr, 'timeout'
            self.readability(webview)
        return True
    
    def bye(self):
        gtk.main_quit()
        sys.exit(0)

def get_cmd_options():
    """
    gets and validates the input from the command line
    """
    parser = OptionParser("usage: %prog [options]")
    
    parser.add_option('-u', '--url', dest='url', help='URL to extract the article from.')
    parser.add_option('-b', '--browser', action="store_true", dest='browser', default=False, help='Show the browser window. Default is False.')
    parser.add_option('-i', '--images', action="store_true", dest='images', default=False, help='Enable image loading inside the webkit browser, it doesn\'t affect the article extraction.')
    parser.add_option('-v', '--java', action="store_true", dest='java', default=False, help='Enable java applets inside the webkit browser, it doesn\'t affect the article extraction.')
    #parser.add_option('-j', '--javascript', action="store_true", dest='javascript', default=False, help='Enable javascript inside the webkit browser, it doesn\'t affect the article extraction.')
    parser.add_option('-p', '--plugins', action="store_true", dest='plugins', default=False, help='Enable plugins inside the webkit browser, it doesn\'t affect the article extraction.')
    (options,args) = parser.parse_args()
 
    if not options.url: 
        raise Exception('You must specify an URL.',sys.argv[0],'--help for more details') 
    return options

def main():
    options = get_cmd_options()
    gtkcrawler = GtkCrawler(options)
    gtkcrawler.run()

if __name__ == '__main__':
    main()