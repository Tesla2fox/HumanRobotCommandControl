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

import sys



def HRCC_opt():
    np.random.seed(0)
#    print(np.random.rand(1,50) * 50)
    arrTimeArray = np.random.rand(100) * 4
#    print(arrTimeArray)
    arrTypeArray = np.random.randint(2,size = 100)
    arrIDArray = np.random.randint(15,size = 100)

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
    
    
#    print(arrTypeArray)
    allianceID = np.random.choice(4,15)
    print(allianceID)
#    np.mat()
#    for i in range(len(arrTypeArray)):
#    print(arrTypeLst)
    
    hrcc_opt_solver = HRCC_Opt_Solver(arrTimeLst,arrTypeLst,arrIDLst,allianceID)
#    hrcc_opt_solver.evolution()


class RobSTATUS(Enum):
    '''
    等待开始、等待处理、等待结束
    '''
    arr = 1
    startPro = 2
    endPro = 3    
    stop = 4
    
    
class HRCC_Opt_Solver(object):
    def __init__(self,arrTimeLst,arrTypeLst,arrIDLst,allianceID):
        self.bounds = [(0,1)] * 5
        self.arrTimeLst =  arrTimeLst
        self.arrTypeLst = arrTypeLst        
        self.arrIDLst = arrIDLst 
        self.robArrTime = [[] for x in range(15)]
        
        print(arrTimeLst)
        for i in range(len(self.arrIDLst)):
            arrID = arrIDLst[i]
            print(arrID)
            self.robArrTime[arrID].append((self.arrTimeLst[i],self.arrTypeLst[i]))
#        print(self.robArrTime)
        self.robStatusLst = [RobSTATUS.arr for robID in range(15)]
        
        self.robEventTimeLst = [self.robArrTime[robID][0][0] for robID in range(15)]
#        print('event',self.robEventTimeLst)
        
        self.robEventIDLst = [0 for robID in range(15)]
        self.robEventMAXNumLst = [len(self.robArrTime[robID]) for robID in range(15)]
        self.allianceID = allianceID
        self.robCmpTimeLst = [0 for robID in range(15)]
        
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
            print('eventID',eventID)
            eventID = eventID + 1
            if eventID > 10:
                raise Exception()
            activeRobID  = self.findEvent()
            if self.robStatusLst[activeRobID] == RobSTATUS.arr:                
                activeRobEventID = self.robEventIDLst[activeRobID]
                robArrTime = self.robArrTime[activeRobID]
                _taskType = robArrTime[activeRobEventID][1]
                _eventTime = self.robEventTimeLst[activeRobID]
                humID,cMode = hrccSol.tempAllocation(activeRobID,_taskType,_eventTime)
                _preTime = hrccSol.generateRealStartTime(humID,activeRobID,cMode,_eventTime)
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
        def minFunc(p):
            return p[1]        
        robEventTime = min(enumerate(self.robEventTimeLst),key = minFunc)
        eventRobID = robEventTime[0]
        return eventRobID
        
    def calMakespan(self):
        return max(self.robCmpTimeLst)
    def endAllEvent(self):
                
        if RobSTATUS.arr in self.robStatusLst or RobSTATUS.startPro in self.robStatusLst or RobSTATUS.endPro in self.robStatusLst:
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