import pandas as pd
import os 

path=r'C:\earning_calendar\quarter'
files=os.listdir(path)
filesPath=[os.path.join(path,f) for f in files]
for i in range(len(filesPath)):
    line=open(filesPath[i]).read().split('\n')[:-1]
    date=[int(l[:8]) for l in line]
    stock=[s[-9:] for s in line]
    df=pd.DataFrame({'stock':stock},index=date)
    df=df.sort()
    f=open(r'c:\earning_calendar\quarter4\%s.txt'%files[i][:-4],'w')
    for c in range(len(df)):
        f.write('%s\t%s\n'%(df.index[c],df.iat[c,0]))
    f.close()