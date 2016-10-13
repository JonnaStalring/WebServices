import os
import redis
from rq import Worker, Queue, Connection

def killProcessByName(processName):
    import subprocess
    print "Current process ID ", os.getpid()
    currPid = os.getpid()
    p = subprocess.Popen(['ps', '-eaf'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if processName in line:
            print "Killing process..."
            print line
            pid = int(line.split()[1])
            if pid != currPid:
                os.system("kill -9 "+ str(pid))


listen = ['default']

#redis_url = os.getenv('RDB_PORT_6379_TCP', 'redis://localhost:6379')
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    print 'Killing old worker processes'
    processName = 'RQworkerChemics' 
    killProcessByName(processName)

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()

