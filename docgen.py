'''Generate documentation for crawler modules'''

import os,subprocess,utilities,sys,glob
from epydoc.cli import cli

args=[]
args.append('--debug')
args.append('--name=Metadata Crawler')
args.append('--css=white')
args.append('--output=%s\\doc\\files'%os.environ['CURDIR'])
#args.append('--top=index.html')
args.append('--html')
args.append('--verbose')
args.append('--show-private')
args.append('--show-imports')

args.append('%s\\runcrawler.py'%os.environ['CURDIR'])
args.append('%s\\runtransform.py'%os.environ['CURDIR'])

for py in utilities.rglob('%s\\lib'%os.environ['CURDIR'],'*.py'):
    args.append(py)
sys.argv.extend(args)
cli()

#Copy the index.html frameset file one level up
html=open('%s\\doc\\files\\index.html'%os.environ['CURDIR']).read()
index=open('%s\\doc\\index.html'%os.environ['CURDIR'],'w')
index.write(html.replace('src="','src="files/'))
index.close()