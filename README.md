my-reading
==========

Experiments in pulling data from my Zotero daily reading library (via the Zotero readapi), serializing that information as Markdown, and then pushing it to Tumblr via email.

I run this under Python 2.7 in a virtual environment with the following packages installed via pip:

chardet==2.1.1
feedparser==5.1.3
html2text==3.200.3
httplib2==0.8
lxml==3.2.4
wsgiref==0.1.2

The code also makes use of the libzotero package. At present, this is imported from the local disk (see lines 24 and 25 in latest.py, which you'll need to change to get it running) because at the time I was last making modifications, I needed a locally patched version of libZotero. Those changes have since been supplied back and merged into libZoter, but I haven't had a chance to back out this modification and check with the installed distro of the package.

You'll also need to take the creds-template.json file and customize it for your configuration and save it as creds.json. This will contain various private items like your Zotero API key, which library you want to target, and so forth, as well as the email accounts, smtp server, tumblr accounts, etc.

Run as follows:

python latest.py 

It runs with log level set to "info". Passing -v on the command line will set log level to "debug".

Lines 252-298 of latest.py have most of the zotero interaction in them.
