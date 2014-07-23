# Copyright (c) 2011 Australian Government, Department of Sustainability, Environment, Water, Population and Communities
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Usage:
batchdelete_jpgmefxml.py [options]
Options:
  -h, --help  show this help message and exit
  -x xls      The crawler result spreadsheet containing images marked as deleted
  -d dir      MEF and XML dir

Warning this will delete all JPG and MEF/XML files if they don't exist in the
results spreadsheet!
'''
import sys,glob,os
from metageta import utilities  as mgutils

def main(xls,xmldir):
    xlrdr = mgutils.ExcelReader(xls)
    qlkdir=os.path.dirname(xls)
    keepers=[]
    for rec in xlrdr:
        if not rec.get('DELETED',0) in [1,'1']:
            basename=os.path.join(xmldir,rec['filename']+'.'+rec['guid'])
            keepers.append(os.path.join(qlkdir,rec['quicklook']))
            keepers.append(os.path.join(qlkdir,rec['thumbnail']))
            keepers.append(basename+'.mef')
            keepers.append(basename+'.xml')

    exts=['*.jpg','*.xml','*.mef']
    for ext in exts:
        for f in glob.glob(os.path.join(qlkdir,ext)):
            if f not in keepers:
                os.unlink(f)
                print(f)

    pass

if __name__ == '__main__':
    import optparse

    description='Batch delete quicklooks and xml that are not in an existing crawl results spreadsheet.'
    parser = optparse.OptionParser(description=description)
    parser.add_option('-x', dest="xls", metavar="xls",
                      help='The crawler result spreadsheet containing images marked as deleted')
    parser.add_option("-d", dest="xmldir", metavar="xmldir",
                      help="MEF and XML dir")
    opts,args = parser.parse_args()
    kwargs={}
    if not opts.xls or not opts.xmldir:
        print
        parser.print_help()
    else:
        main(opts.xls,opts.xmldir)

    try:usr = raw_input("Press <Enter> to exit")
    except:pass
