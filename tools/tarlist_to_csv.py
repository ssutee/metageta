import glob,os.path
out=open('../docs/tarlist.csv','w')
out.write(','.join(['tape','path','priv','user','size','date','time'])+'\n')
for f in glob.glob('../docs/*.tarlist'):
    print f
    tapeid=os.path.basename(f).split('.')[0]
    for i,line in enumerate(open(f,'r')):
        line=line.strip().split()
        priv,user,size,mdate,mtime = line[0:5]
        path = ' '.join(line[5:])
        if int(size) > 0:out.write(','.join([tapeid,'"'+path+'"',priv,user,size,mdate,mtime])+'\n')
        out.flush()
out.close()