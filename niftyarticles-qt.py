#!/usr/bin/env python
"""
------------------------------------
NiftyArticles v0.4, Qt4 version

Made by Florentin Sardan
florentinwww (at) gmail.com

Project's page:
    http://www.betterprogramming.com/niftyarticles-extract-articles-from-any-webpage-with-python-webkit-and-readability.html
My portfolio:
    http://www.betterprogramming.com/

Readability webpage:
    http://lab.arc90.com/experiments/readability/
------------------------------------
The script has been developed and tested on Python 2.6.6 / Ubuntu Maverick

Install the required packages: python-qt4 libqt4-webkit
Ubuntu or Debian
sudo apt-get install python2.6 python-qt4 libqt4-webkit

(Optional) Mark the script as executable
chmod +x niftyarticles-qt.py

Usage Examples:
python niftyarticles-qt.py --help

# save an article from ubuntu.com
python niftyarticles-qt.py -u http://www.ubuntu.com/project/derivatives

# show the browser window, load images, enable java applets 
python niftyarticles-qt.py -b -i -v -u http://www.ubuntu.com/project/canonical-and-ubuntu

# to run the script on a server with no GUI available, you must install xvfb
sudo apt-get install xvfb
# then you can do 
xvfb-run -a python niftyarticles-qt.py -u http://www.ubuntu.com/project/derivatives

Webkit Reference
http://webkitgtk.org/reference/index.html

"""
import sys, time, signal
import urllib2, urlparse
from optparse import OptionParser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebPage, QWebView, QWebSettings

signal.signal(signal.SIGINT, signal.SIG_DFL)

class WebPage(QWebPage):
    def __init__(self):
        super(WebPage, self).__init__()
    
    def readability(self):
        if getattr(self, 'extraction_in_progress', None): return True
        
        websettings = self.settings()
        websettings.setAttribute(QWebSettings.JavascriptEnabled, True)
        
        #readability_code = """(function(){readConvertLinksToFootnotes=false;readStyle='style-newspaper';readSize='size-medium';readMargin='margin-wide';_readability_script=document.createElement('script');_readability_script.type='text/javascript';_readability_script.src='http://lab.arc90.com/experiments/readability/js/readability.js?x='+(Math.random());document.documentElement.appendChild(_readability_script);})();"""
        with open('readability.js', 'r') as f:
            readability_code = f.read()
        
        script = """
        readConvertLinksToFootnotes=false;readStyle='style-newspaper';readSize='size-medium';readMargin='margin-wide';
        """+readability_code+""";
        function timedCount() {
            var readability_content = document.getElementById("readability-content");
            if (readability_content) {
                var title = document.title;
                var body = readability_content.innerHTML;
                clearTimeout(intervalID);
                MainWindow.js_article(title, body);
                MainWindow.js_bye();
            };
        };
        var intervalID = setInterval("timedCount()", 1000);
        var timeoutID = setTimeout("MainWindow.js_bye();", 5000); // exit after 5 seconds
        """
        setattr(self, 'extraction_in_progress', True)
        result = self.mainFrame().evaluateJavaScript(script)
  
    def javaScriptAlert(self, frame, msg):
        content = str(msg.toUtf8())
        print >> sys.stderr, 'alert', content
 
class Application(QApplication):
    def __init__(self, options):
        super(Application, self).__init__(sys.argv)
        self.web_page = WebPage()
        
        websettings = self.web_page.settings()
        websettings.setAttribute(QWebSettings.AutoLoadImages, options.images)
        websettings.setAttribute(QWebSettings.JavaEnabled, options.java)
        websettings.setAttribute(QWebSettings.JavascriptEnabled, True)
        websettings.setAttribute(QWebSettings.PluginsEnabled, options.plugins)
        
        self.main_frame = self.web_page.mainFrame()

        if options.browser:
            self.web_view = QWebView()
            self.web_view.setPage(self.web_page)
            self.web_view.show()
    
    @pyqtSlot()
    def js_onload(self):
        self.web_page.readability()
    
    @pyqtSlot(QVariant, QVariant)
    def js_article(self, title, body):
        print title.toString().toUtf8()
        print body.toString().toUtf8()
    
    @pyqtSlot()
    def js_bye(self):
        self.exit()
        sys.exit(0)
    
    def load(self, url):
        #self.main_frame.load(QUrl(url))

        f = urllib2.urlopen(url)
        html = f.read()
        f.close()
        o = urlparse.urlparse(url)
        self.main_frame.setHtml(html, QUrl(o.hostname))
        
        self.main_frame.addToJavaScriptWindowObject("MainWindow", self)
        doc_element = self.main_frame.documentElement()

        doc_element.evaluateJavaScript("""
        var domreadyID = setInterval(function() {
            var state = document.readyState;
            if (state == 'loaded' || state == 'complete') {
                MainWindow.js_onload();
                clearInterval(domreadyID);
            }
        }, 50);
        window.setTimeout("MainWindow.js_onload();", 10000); // if nothing happens for 10 seconds
        """)
        self.exec_()

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
    app = Application(options)
    sys.exit(app.load(options.url))

if __name__ == '__main__':
    main()
