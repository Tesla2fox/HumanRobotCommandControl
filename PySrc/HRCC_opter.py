# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:17:54 2019

@author: robot
"""


import HRCC
import Robot
import Human

from Robot import TaskType

from scipy.optimize import differential_evolution 
import numpy as np
import random
from MyDifferentialEvolution import my_differential_evolution
from HRCC import HRCCSOL

import HRCC 

from enum import Enum
from collections import namedtuple

import sys


RobEventTuple = namedtuple('RobEventTuple',['arrTime','startTime','endTime'])

def HRCC_opt():
    
    eventNum = 10
    humNum = 2    
    robotNum = 4

    np.random.seed(0)
#    print(np.random.rand(1,50) * 50)
    arrTimeArray = np.random.rand(eventNum) * eventNum
#    print(arrTimeArray)
    arrTypeArray = np.random.randint(2,size = eventNum)
    arrIDArray = np.random.randint(robotNum,size = eventNum)


    arrTimeLst = []
    arrIDLst = []
    arrTypeLst = []

    
    for i in range(arrTimeArray.size):
        arrTimeLst.append(arrTimeArray[i])
        arrIDLst.append(arrIDArray[i])
        if arrTypeArray[i] == 0:
           arrTypeLst.append(TaskType.Aggregation)
        if arrTypeArray[i] == 1:
           arrTypeLst.append(TaskType.Surveillance)

    print(arrTypeLst)    
    
#    print(arrTypeArray)
    allianceID = np.random.choice(humNum,robotNum)
    
#    raise Exception('wtf')
    print(allianceID)
#    np.mat()
#    for i in range(len(arrTypeArray)):
#    print(arrTypeLst)
    
    
    
    hrcc_opt_solver = HRCC_Opt_Solver(arrTimeLst,arrTypeLst,arrIDLst,allianceID,humNum,robotNum)
#    hrcc_opt_solver.evolution()


class RobSTATUS(Enum):
    '''
    等待开始、等待处理、等待结束
    '''
    arr = 1
    startPro = 2
    endPro = 3    
    stop = 4
    

class RealRobEvent(object):
    def __init__(self):        
        self._eventTypeLst  = []
        self._eventTimeLst = []
#    self.    
        self._c_status = RobSTATUS.stop
        self._c_eventTime = sys.float_info.max
        self._c_taskType = TaskType.noTask
        self._c_eventStartProTime = sys.float_info.max
        self._c_eventEndProTime = sys.float_info.max
        self._c_eventArrTime = sys.float_info.max
        
        self._c_taskID = 0

        self._maxTaskNum = 0
        self._cmpTime = sys.float_info.max        
    
class HRCC_Opt_Solver(object):
    def __init__(self,arrTimeLst,arrTypeLst,arrIDLst,allianceID,humNum,robNum):
        self.bounds = [(0,1)] * 5
        self.arrTimeLst =  arrTimeLst
        self.arrTypeLst = arrTypeLst        
        self.arrIDLst = arrIDLst 
        self._humNum = humNum
        self._robNum = robNum
        self._eventNum = len(self.arrIDLst)
        
        
        
        self._realRobEventLst = []        
        for robID in range(self._robNum):
            robEvent = RealRobEvent()
            self._realRobEventLst.append(robEvent)
            
        
        for i in range(self._eventNum):
            arrID = arrIDLst[i]
            print(arrID)
            robEvent = self._realRobEventLst[arrID]
            robEvent._eventTimeLst.append(self.arrTimeLst[i])
            robEvent._eventTypeLst.append(self.arrTypeLst[i])
            
            
        for robEvent in self._realRobEventLst:
            if  robEvent._eventTypeLst:
                robEvent._c_status = RobSTATUS.arr
                robEvent._c_eventTime = robEvent._eventTimeLst[0]
                robEvent._c_taskType = robEvent._eventTypeLst[0]
                robEvent._maxTaskNum = len(robEvent._eventTimeLst)
#                robEvent._c_status = RobSTATUS.endPro
#                robEvent._c_eventTime = robEvent._c_eventTime[0]
#            else:
#                robEvent._c_e
                
        
        self.allianceID = allianceID
        
        x = [2,1,4,3,2]
        
        self.calFitness(x)
                
    def calFitness(self,x):
        
        
        arrEventID = 0
        endEventID = 0
        
        hrccSol = HRCCSOL()

        hrccSol._inAllRate = x[0]
        hrccSol._outAllRate = x[1]
        hrccSol._inWorkEffZone = x[2]
        hrccSol._outWorkEffZone = x[3]
        hrccSol._beyondWorkZone = x[4]

        hrccSol._saveBool = True
        
        hrccSol.initAllocation(self.allianceID)
        
        eventID = 0
        while not self.endAllEvent():
#            print('eventID',eventID)
            eventID = eventID + 1
            if eventID > 10:
                raise Exception()
            activeRobID  = self.findEvent()
            print('actRobID = ',activeRobID)
            robEvent = self._realRobEventLst[activeRobID]            
            
            if robEvent._c_status == RobSTATUS.arr:                
                _eventTime = robEvent._c_eventArrTime
                _eventTime = robEvent._c_taskType
                
                activeRobEventID = self.robEventIDLst[activeRobID]
#                robArrTime = self.robArrTime[activeRobID]
#                _taskType = robArrTime[activeRobEventID][1]
#                _eventTime = self.robEventTimeLst[activeRobID]
                _eventTime,_taskType = self._robEventArrTime[activeRobID][activeRobEventID]                
                humID,cMode = hrccSol.tempAllocation(activeRobID,_taskType,_eventTime)
                
                        
                startProTime = hrccSol.generateRealStartTime(humID,activeRobID,cMode)                
                endProTime = hrccSol.generateRealEndTime(humID,activeRobID,cMode,_eventTime)
                
#                _preTime = hrccSol.generateRealStartTime(humID,activeRobID,cMode,_eventTime)
#                _
                self.robEventTimeLst[activeRobID] = _preTime
#                _preTime = hrccSol.generateProTime(humID,activeRobID,cMode)                
#                self.robEventTimeLst[activeRobID] = self.robEventTimeLst[activeRobID] + _preTime
#                self.robStatusLst[activeRobID] =     RobSTATUS.ready_end                
                self.robStatusLst[activeRobID] = RobSTATUS.startPro
            else:
                if self.robStatusLst[activeRobID] == RobSTATUS.startPro:
                    
                    
                    
                    
                    
                    
                    self.robStatusLst[activeRobID] = RobSTATUS.endPro                    
                    pass                
                else:                        
                    self.robEventIDLst[activeRobID] = self.robEventIDLst[activeRobID] + 1
                    hrccSol.elimate(activeRobID,self.robEventTimeLst[activeRobID])
    
                    if self.robEventIDLst[activeRobID] == self.robEventMAXNumLst[activeRobID]:
                        self.robCmpTimeLst[activeRobID] = self.robEventTimeLst[activeRobID]
                        self.robEventTimeLst[activeRobID] = sys.float_info.max
                        self.robStatusLst[activeRobID] = RobSTATUS.stop
                        continue
                    else:
    #                    print(self.robArrTime[activeRobID][self.robEventIDLst[activeRobID]][0])
                        self.robEventTimeLst[activeRobID] = self.robEventTimeLst[activeRobID] +\
                                                    self.robArrTime[activeRobID][self.robEventIDLst[activeRobID]][0]
                        self.robStatusLst[activeRobID] = RobSTATUS.arr


        print(self.calMakespan())                                
        pass
                
#            hrccSol.tempAllocation(1,TaskType.Aggregation,0)
            
#        while arrEventID
#        arg1 = -0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))
#        arg2 = 0.5 * (np.cos(2. * np.pi * x[0]) + np.cos(2. * np.pi * x[1]))
#        return -20. * np.exp(arg1) - np.exp(arg2) + 20. + np.e
            
        pass
    
    def findEvent(self):
        
        eventTime = sys.float_info.max
        
        for robID in range(self._robNum):
            robEvent = self._realRobEventLst[robID]
            if robEvent._c_status == RobSTATUS.arr:
                if robEvent._c_eventTime < eventTime:
                    eventRobID = robID
            if robEvent._c_status == RobSTATUS.startPro:
                if robEvent._c_eventTime < eventTime:
                    eventRobID = robID
            if robEvent._c_status == RobSTATUS.endPro:
                if robEvent._c_eventTime < eventTime:
                    eventRobID = robID
                
#        for robID in range(self._robNum):
#            if self.robStatusLst[robID] == RobSTATUS.arr:
#                if self.robEventTupleLst[robID].arrTime < eventTime:
#                    eventRobID = robID
#            if self.robStatusLst[robID] == RobSTATUS.startPro:
#                if self.robEventTupleLst[robID].startTime < eventTime:
#                    eventRobID = robID
#            if self.robStatusLst[robID] == RobSTATUS.endPro:
#                if self.robEventTupleLst[robID].endTime < eventTime:
#                    eventRobID = robID
                    
#        def minFunc(p):
#            return p[1]        
#        robEventTime = min(enumerate(self.robEventTimeLst),key = minFunc)
#        eventRobID = robEventTime[0]
        return eventRobID
        
    def getEventStartProRealTime(self,humID,_eventTime):        
        return _eventTime +  random.random() * 3

    def getEventProRealTime(self,humID,_eventTime):        
        return  random.random() * 2        

    def calMakespan(self):
        return max(self.robCmpTimeLst)
    
    def endAllEvent(self):        
        for robEvent in self._realRobEventLst:
            if robEvent._c_status != RobSTATUS.stop:
                return False
            else:
                return True
        
    def evolution(self):
        result = my_differential_evolution(self.calFitness,self.bounds,drawPlotBool = False)
        print(result.x,result.fun)
        
#    def drawFitnessPlot(self):
        
    
        
        

        
        
        
if __name__ == '__main__':
    bounds = [(0,1)] *5
#    print(bounds)       
    HRCC_opt()
#    hrcc_opt = HRCC_Opt()
#    hrcc_opt.evolution()