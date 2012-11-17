# -*- coding: utf-8 -*-

from binascii import *
import sys, math, time

class ConsistentHashing():
    '''
    Class implements algorithm used in php-memcache module.
    Taken from version 3.0.5/3.0.6
    '''
    def __init__(self, nodes=[], consistent_points = 160, consistent_buckets = 1024, weight = 1):
        '''
        @param nodes: Server list in ip:port format"
        @param consistent_points: point for server
        @param consistent_buckets: buckets count
        @param weight: weight for servers
        
        @author Malinowski
        '''

        ''' Check variable types '''
        assert(isinstance(nodes, list))
        assert(isinstance(consistent_points, int))
        assert(isinstance(consistent_buckets, int))
        assert(isinstance(weight, int))

        self.serversList = nodes
        self.weight = weight
        self.consistentPoints = consistent_points
        self.consistentBuckets = consistent_buckets
        
        self.points = {}
        self.sortedPointsKeys = None
        
        self.buckets = {}
        
        ''' Adding servers '''
        for server in nodes:
            self.__addServer(server)
            
        self.__populateBuckets()
        
    def __populateBuckets(self):
        '''
        For every bucket list server
        @author Malinowski
        '''
        
        ''' If sorted points list was not created then take keys and sort '''
        if self.sortedPointsKeys == None:
            self.sortedPointsKeys = sorted(self.points.keys())
        
        ''' point we are searching for '''
        pointSearch = 0xffffffff / self.consistentBuckets

        ''' select server for each bucket '''
        for bucketNumber in xrange(self.consistentBuckets):
            self.buckets[bucketNumber] = self.__consistentFind(pointSearch * bucketNumber)
        
    def __consistentFind(self, pointSearch):
        '''
        Search server for a given bucket
        @param pointSearch: searched value
        '''
        
        pointStart = 0
        pointLast = len(self.points) - 1

        ''' Try to find exact value '''
        try:
            testSearch = self.sortedPointsKeys.index(pointSearch)
            return testSearch
        except:
            pass
        
        
        ''' If value is outside the range then return first server '''
        if pointSearch <= self.sortedPointsKeys[0] or pointSearch > self.sortedPointsKeys[pointLast]:
            return self.points[self.sortedPointsKeys[0]]

        ''' Binary search '''
        while True:
            pointMiddle = int(math.floor(pointStart + ((pointLast-pointStart)/float(2))))
            
            if pointSearch > self.sortedPointsKeys[pointMiddle]:
                pointStart = pointMiddle + 1
            else:
                pointLast = pointMiddle - 1
            
            if self.sortedPointsKeys[pointMiddle - 1] < pointSearch and pointSearch <= self.sortedPointsKeys[pointMiddle]:
                return self.points[self.sortedPointsKeys[pointMiddle]]
        
    def __addServer(self, serverData):
        '''
        Adding server to list
        @param serverData: single server "ip:port"
        '''
        
        ''' Points for every server '''
        pointsLength = self.weight * self.consistentPoints
        
        '''
        Kill me but i have no idea why in php module there is "-" sign on the end of server
        key_len = sprintf(key, "%s:%d-", mmc->host, mmc->tcp.port);
        '''
        serverHash = crc32(serverData+'-') & 0xffffffff
    
        ''' For every point from 0 to pointsLength we create hash connected with server hash '''
        for singlePoint in xrange(pointsLength):
            point = crc32(str(singlePoint), serverHash) & 0xffffffff

            self.points[point] = serverData
    
    def addServer(self, serverData):
        '''
        Method to add new server and rearrenge buckets.
        @author Malinowski
        '''
        if type(serverData) is type([]):
            for server in serverData:
                self.__addServer(server)
        elif type(serverData) is type(str()):
            self.__addServer(serverData)
        else:
            raise TypeError("String or list")
            
        self.__populateBuckets()
    
    def findServer(self, key):
        '''
        Search server for key
        @param key: String key
        '''
        
        assert(isinstance(key, str))
        
        ''' If there is only 1 server return it '''
        if len(self.serversList) == 1:
            return self.serversList[0]
        ''' policzenie hasha i zwrócenie odpowiedniego serwera '''
        hash = crc32(str(key)) & 0xffffffff
        return self.buckets[hash % self.consistentBuckets]