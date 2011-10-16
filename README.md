# csstty

cssselect.py is a patched version of
[lxml.cssselect](http://lxml.de/cssselect.html) to handle a default
namespace.

# Running CSS Test Suite

There is an official W3C [CSS Test Suite](http://test.csswg.org/).
You can get it with [Mercurial](http://mercurial.selenic.com/).

    hg clone http://hg.csswg.org/test/
    ln -s test/approved/css2.1/src css21

Some tests even pass on csstty! You can run an individual test like
this:

    python csstty.py css21/box-display/display-001.xht

Tests that the author has confirmed to pass are listed in PASS file.
