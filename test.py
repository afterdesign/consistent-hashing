# -*- coding: utf-8 -*-
from consistent import ConsistentHashing
from hashlib import md5

servers = ["10.0.1.6:11211", "10.0.1.7:11211"]
a=ConsistentHashing(servers)

#print "for %d server %s" % (0, a.findServer(md5(str(0)).hexdigest()))
for i in xrange(0,10):
    print "for %d server %s" % (i, a.findServer(md5(str(i)).hexdigest()))