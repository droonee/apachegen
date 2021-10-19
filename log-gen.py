#!/usr/bin/python
import time
import datetime
import pytz
import numpy
import random
import gzip
import zipfile
import sys
import argparse
from faker import Faker
from random import randrange
from tzlocal import get_localzone
local = get_localzone()

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--output", "-o", dest='output_type', help="Write to a Log file, a gzip file or to STDOUT", choices=['LOG','GZ','CONSOLE'] )

args = parser.parse_args()

output_type = args.output_type

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now() - datetime.timedelta(hours=1)

outFileName = 'access.log'

for case in switch(output_type):
    if case('LOG'):
        f = open(outFileName,'w')
        break
    if case('GZ'):
        f = gzip.open(outFileName+'.gz','w')
        break
    if case('CONSOLE'): pass
    if case():
        f = sys.stdout

response=["200","404","500","301","401","303"]
verb=["GET","POST","DELETE","PUT","PATCH"]
resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]
ualist=["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/43.0.845.0 Safari/534.1", "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_8 like Mac OS X) AppleWebKit/536.2 (KHTML, like Gecko) FxiOS/17.5h1393.0 Mobile/09X753 Safari/536.2", "iPad; CPU iPad OS 12_4_8 like Mac OS X", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_8 rv:3.0; kk-KZ) AppleWebKit/531.6.3 (KHTML, like Gecko) Version/5.0.1 Safari/531.6.3", "Opera/9.61.(X11; Linux x86_64; az-IN) Presto/2.9.190 Version/12.00"]

num_logs = [1,5,20,40,80,100]
log_lines = 1
flag = True
while (flag):
    increment = datetime.timedelta(seconds=random.randint(1, 2))
    otime += increment

    ip = faker.ipv4()
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(local).strftime('%z')
    vrb = numpy.random.choice(verb,p=[0.6,0.1,0.05,0.2,0.05])

    uri = random.choice(resources)
    if uri.find("apps")>0:
        uri += str(random.randint(1000,10000))

    resp = numpy.random.choice(response,p=[0.8,0.04,0.02,0.04,0.05,0.05])
    byt = int(random.gauss(5000,50))
    referer = faker.uri()
    useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05])

    f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip,dt,tz,vrb,uri,resp,byt,referer,useragent))
    f.flush()

    log_lines = log_lines - 1
    if log_lines == 0:
        log_lines = numpy.random.choice(num_logs,p=[0.05,0.3,0.3,0.2,0.1,0.05])
        sleeptime = random.uniform(3.0,8.0)
        time.sleep(sleeptime)
