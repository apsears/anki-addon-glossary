from anki.hooks import wrap
from anki.sync import Syncer
from anki.lang import _
from anki.exporting import TextCardExporter

import re
import os

TARGETFOLDER = './s3'
# S3BUCKET = os.environ['S3BUCKET']
NCARDS = 20

class MyTextCardExporter(TextCardExporter):
    key = _("Export deck as Html Glossary")
    ext = ".htm"
    hideTags = True
    htmlBefore = """
<!DOCTYPE html PUBLIC "-/W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<style type="text/css">


.Question{
    float: left;
    height: auto;
    width: 30%;
}
.Answer{
    float: right;
    height: auto;
    width: 30%;
}

.Answer,.Question{
    overflow: auto;
    padding:4px;
    position: relative;
    visibility: visible;
    height: auto;
}
.Card {
    min-width:25px;
    text-align: center;
    clear:both;
    height: auto;
    width: 640px;
    overflow: visible;
    border-top-width: thin;
    border-right-width: thin;
    border-bottom-width: thin;
    border-left-width: thin;
    border-top-style: solid;
    border-right-style: solid;
    border-bottom-style: solid;
    border-left-style: solid;
    display: block;
}

.Card:after {
    content: '.';
    display: block;
    clear: both;
    visibility: hidden;
    height: 0;
    line-height: 0;
}
img {
    max-height: 400px;
    max-width: 400px;
    display: compact;
    margin: 0px;
    padding: 1px;
    top:0;
    left:0;
}



</style>
<link type="text/css" rel="stylesheet" href="custom.css">
</head>
<body style="font-size:200%">
    """
    htmlAfter = """
    </body>
</html>
    """

    def __init__(self, col):
        TextCardExporter.__init__(self, col)

    def escapeText(self, text):
        "Escape newlines, tabs and CSS."
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = re.sub("(?i)<style>.*?</style>", "", text)
        return text

    def doExport(self, file):
        cards = self.cardIds()

        def esc(s):
            # strip off the repeated question in answer if exists
            s = re.sub("(?si)^.*<hr id=answer>\n*", "", s)
            s = re.sub("(?si)<style.*?>.*?</style>", "", s)
            return self.escapeText(s)

        out = ""

        for c in cards:
            if c:
            # c = self.col.getCard(cid)
                out += "<div class=Card>"
                out += "  <div class=Question>" + esc(c.q()) + "</div>"
                out += "  <div class=Answer>" + esc(c.a()) + "</div>"
                out += "</div>"
        out = self.htmlBefore + out + self.htmlAfter
        file.write(out.encode("utf-8"))

    def cardIds(self):
        cardList = [self.col.sched.getCard() for _ in range(NCARDS)]
        cardList = filter(lambda x: x, cardList)

        for _ in range(NCARDS - len(cardList)):
            cardList.append(self.col.sched._getLrnCard())
        cardList = filter(lambda x: x, cardList)

        for _ in range(NCARDS - len(cardList)):
            cardList.append(self.col.sched._getRevCard())
        cardList = filter(lambda x: x, cardList)


        return sorted(cardList, key=lambda x: x.template(), reverse=False)

def exportScheduled(self):
    exp = MyTextCardExporter(self.col)
    path = os.path.join(TARGETFOLDER,'scheduledVocab.html')
    file = open(path, "wb")
    exp.doExport(file)
    # os.system("aws s3 sync --acl public-read %s s3://%s" % (TARGETFOLDER, S3BUCKET))
    return "success"


Syncer.sync = wrap(Syncer.sync, exportScheduled)
