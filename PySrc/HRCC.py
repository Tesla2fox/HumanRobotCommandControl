# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:52:44 2019

@author: robot
"""

import numpy as np
import numpy
import random
from Human import Human
from Human import ControlMode
from Robot import Robot
from Robot import TaskType
import copy

#import Human


class HRCCSOL:
    def __init__(self):
        self._robNum = 15
        self._humNum = 4        
        self._humLst = [Human(i) for i in range(self._humNum)]
        self._robLst = [Robot(i) for i in range(self._robNum)]
        self._humStartProTime = [0 for i in range(self._humNum)]
        
        
        '''
        some para need opt
        '''
        self._inAllRate = 1
        self._outAllRate = 2
        self._inWorkEffZone = 3
        self._outWorkEffZone = 4
        self._beyondWorkZone = 5
        
        
#        for i in range(15):            
#            print(self._robLst[i])
    
    def initAllocation(self,allianceID):
        self._allianceID = copy.copy(allianceID)
#        for x in allianceID:        
        pass
    
    def getPredictMakespan(self,humID,predictEndProTime):
        _predictLst = copy.copy(self._humStartProTime)
        _predictLst[humID] = predictEndProTime
        return max(_predictLst)
    
    def tempAllocation(self,robID,taskType,arrTime):
        fitnessLst = []
        for humID in range(self._humNum):
            fitness = self.calFitness(robID,humID,ControlMode.MBC,taskType,arrTime)
            fitnessLst.append((humID,ControlMode.MBC,fitness))

            fitness = self.calFitness(robID,humID,ControlMode.MBE,taskType,arrTime)
            fitnessLst.append((humID,ControlMode.MBE,fitness))
        
        def minFunc(p):
            return p[2]
        
        minFitness = min(fitnessLst,key = minFunc)
        
        minHumID = minFitness[0]
        cMode = minFitness[1]
        self.update(minHumID,robID,cMode,taskType,arrTime)
        
        print(minFitness)

    def update(self,humID,robID,cMode,taskType,arrTime):
        hum = self._humLst[humID]
        rob = self._robLst[robID]
        if taskType ==  TaskType.Aggregation:            
            if cMode == ControlMode.MBC:
                increWorkLoad = 2
            if cMode == ControlMode.MBE:
                increWorkLoad = 1
        if taskType == TaskType.Surveillance:
            if cMode == ControlMode.MBC:
                increWorkLoad = 3
            if cMode == ControlMode.MBE:
                increWorkLoad = 2
        hum._cWorkLoad = hum._cWorkLoad + increWorkLoad
        hum._cRobLst.append(robID)
        rob._taskType = taskType
        rob._controlMode = cMode
        rob._humID = humID
                
    def elimate(self,robID,eliminationTime):
        rob = self._robLst[robID]
        hum = self._humLst[rob._humID]
        if taskType ==  TaskType.Aggregation:            
            if cMode == ControlMode.MBC:
                eliminateWorkLoad = 2
            if cMode == ControlMode.MBE:
                eliminateWorkLoad = 1
        if taskType == TaskType.Surveillance:
            if cMode == ControlMode.MBC:
                eliminateWorkLoad = 3
            if cMode == ControlMode.MBE:
                eliminateWorkLoad = 2
        
        hum._cWorkLoad =  hum._cWorkLoad - eliminateWorkLoad        
        hum._cRobLst.remove(robID)
        
        
                        
        
        
#        sorted()
#        if taskType == TaskType.Aggregation:
            
            
    
    
    def calFitness(self,robID,humID,cMode,taskType,arrTime):
        hum = self._humLst[humID]
        rob = self._robLst[robID]
        if taskType ==  TaskType.Aggregation:            
            if cMode == ControlMode.MBC:
                increWorkLoad = 2
            if cMode == ControlMode.MBE:
                increWorkLoad = 1
        if taskType == TaskType.Surveillance:
            if cMode == ControlMode.MBC:
                increWorkLoad = 3
            if cMode == ControlMode.MBE:
                increWorkLoad = 2
                        
        workEff  = hum.getWorkEfficieny(hum._cWorkLoad + increWorkLoad,hum._cFatigue)                
        predictProTime =  hum.getPredictProcessTime(workEff,taskType)
#        hum.getProcessTime(workEff,taskType)
            
        increFatigue  =  increWorkLoad * predictProTime 
        predictEndProTime = predictProTime + self._humStartProTime[humID]
        predictWorkLoad = hum._cWorkLoad + increWorkLoad
        leftWorkLoad = hum._max_workLoad - predictWorkLoad
        
        preMakespan = self.getPredictMakespan(humID,predictEndProTime)

        predictProDur = preMakespan - arrTime
        
        if predictWorkLoad >= 0 and predictWorkLoad < 7:
            workRate  = self._inWorkEffZone        
        else:
            if predictWorkLoad <=10:                
                workRate = self._outWorkEffZone
            else:
                workRate = self._beyondWorkZone                      
                
        if self._allianceID[robID] == humID:
            allRate = self._inAllRate
        else:
            allRate = self._outAllRate
        
        return workRate*allRate/predictProDur

#        if leftWorkLoad > 0:
            
        
            
#        or taskType == TaskType.Surveillance
    
    




if __name__ == '__main__':
    humIndexLst = [x for x in range(4)]
#    numpy.random.seed = 0
#    random.choice(4,15)
#    np.random.seed(0)    
    allianceID = numpy.random.choice(4,15)
    '''
    numpy random  seed 的 bug 需要解决
    '''
    allianceID = [0,2,3,1,0,3,2,3,0,1,0,2,1,1,2]
    
    
    print(allianceID)
    
#    allianceID =     
        

    
    hrccSol = HRCCSOL()
    hrccSol.initAllocation(allianceID)
    hrccSol.tempAllocation(1,TaskType.Aggregation,0)
    
    
    
#    allianceID[2] = 100
#    print(hrccSol._allianceID)
    