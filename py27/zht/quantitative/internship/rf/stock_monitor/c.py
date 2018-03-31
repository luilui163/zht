import  threading
from Queue import Queue

q=Queue()


for i in range(100):
    q.put(i)

def job(q):
    while not q.empty():
        a=q.get()
        print a,threading.activeCount()


ths=[]
for i in range(5):
    th=threading.Thread(target=job,args=[q])
    ths.append(th)
for i in range(5):
    ths[i].start()
for i in range(5):
    ths[i].join()

print 'test'

