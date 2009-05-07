'''Generate documentation for crawler modules'''

import os,subprocess,utilities,sys
from epydoc.cli import cli

args=[]
args.append('--name=Metadata Crawler')
args.append('--css=blue')
args.append('--output=%s\\doc'%os.environ['CURDIR'])
args.append('--html')
args.append('--verbose')
args.append('--no-private')
args.append('--show-imports')

for py in utilities.rglob('%s\\lib'%os.environ['CURDIR'],'*.py'):
    args.append(py)
sys.argv.extend(args)
cli()