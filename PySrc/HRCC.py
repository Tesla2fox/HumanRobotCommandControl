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
        
        
        self._saveBool = False
        

#        for i in range(15):            
#            print(self._robLst[i])
    
    def initAllocation(self,allianceID):
        if self._saveBool:            
            self._fileDEG = open('_hrcc_DEG.dat','w')    
        self._allianceID = copy.copy(allianceID)
#        for x in allianceID:        
        pass
    
    def generateProTime(self,humID,robID,cMode):        
        hum = self._humLst[humID]
        rob = self._robLst[robID]
        _taskType = rob._taskType
        print('rob._taskType  = ',rob._taskType)
        _workEff = hum.getWorkEfficieny(hum._cWorkLoad,hum._cFatigue)
        proTime = hum.getProcessTime(_workEff,_taskType)                
        return proTime
    
    def generateRealStartTime(self,humID,robID,cMode):

        hum = self._humLst[humID]
        rob = self._robLst[robID]
        _taskType = rob._taskType
        print('rob._taskType  = ',rob._taskType)
        _workEff = hum.getWorkEfficieny(hum._cWorkLoad,hum._cFatigue)
        proTime = hum.getProcessTime(_workEff,_taskType)                

        realStartTime = 1
        
        return realStartTime
        
        
    
    def generateRealEndTime(self,humID,robID,cMode,arrTime):
        proTime = self.generateProTime(humID,robID,cMode)
        if self._humStartProTime[humID] < arrTime:
            beginProTime = arrTime
        else:
            beginProTime = self._humStartProTime[humID]
        realEndTime = beginProTime + proTime
        return realEndTime            
        
    def getPredictMakespan(self,humID,predictEndProTime):
        _predictLst = copy.copy(self._humStartProTime)
        _predictLst[humID] = predictEndProTime
        return max(_predictLst)
    
    def tempAllocation(self,robID,taskType,arrTime):
        fitnessLst = []
        for humID in range(self._humNum):
            fitness,predictEndProTime,predictProTime \
                        = self.calFitness(robID,humID,ControlMode.MBC,taskType,arrTime)
            fitnessLst.append((humID,ControlMode.MBC,fitness,predictEndProTime))

            fitness,predictEndProTime,predictProTime\
                        = self.calFitness(robID,humID,ControlMode.MBE,taskType,arrTime)
            fitnessLst.append((humID,ControlMode.MBE,fitness,predictEndProTime))
        
        def minFunc(p):
            return p[2]
        
#        print(fitnessLst)

        print(sorted(fitnessLst,key = minFunc))
        
        minFitness = max(fitnessLst,key = minFunc)
        
        
        minHumID = minFitness[0]
        cMode = minFitness[1]
        print(minFitness)
        
        print(taskType)
        
        self.update(minHumID,robID,cMode,taskType,arrTime,predictEndProTime,predictProTime)
        
#        print(minFitness)
        
        print(self._humStartProTime)
        return minHumID,cMode
    
    
    def update(self,humID,robID,cMode,taskType,arrTime,predictEndProTime,predictProTime):
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
        self._humStartProTime[humID]  = predictEndProTime        
        rob._taskType = taskType
        rob._controlMode = cMode
        rob._humID = humID
        rob._arrTime = arrTime
        rob._predictProTime = predictProTime
        
        if self._saveBool:
            self._fileDEG.write('HumanWorkLoad '+str(hum._cWorkLoad) + ' humID ' + str( humID)\
                                +' time ' + str(arrTime) + '\n')
            self._fileDEG.flush()
            
                
    def elimate(self,robID,eliminationTime):
        rob = self._robLst[robID]
        hum = self._humLst[rob._humID]
        humID = rob._humID
        taskType = rob._taskType
        cMode = rob._controlMode
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

                        
        self._humStartProTime[humID] = eliminationTime        
        for inQRobID in range(hum._cRobLst):
            inQueueRob =  self._robLst[inQRobID]
            self._humStartProTime[humID] = inQueueRob._predictProTime + self._humStartProTime[humID]
            
#        self._humStartProTime[humID]
                
        if self._saveBool:
            self._fileDEG.write('HumanWorkLoad '+str(hum._cWorkLoad) + ' humID ' + str(rob._humID)\
                                +' time ' + str(eliminationTime) + '\n')
            
            self._fileDEG.write('humID ' + str(rob._humID) + ' robID ' + str(robID) +  \
                                ' start ' + str(rob._arrTime) + ' end ' + str(eliminationTime) + '\n')
            self._fileDEG.flush()
                
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
        if self._humStartProTime[humID] < arrTime:
            predictEndProTime = predictProTime + arrTime            
        else:            
            predictEndProTime = predictProTime + self._humStartProTime[humID]
        
        predictWorkLoad = hum._cWorkLoad + increWorkLoad
        leftWorkLoad = hum._max_workLoad - predictWorkLoad
        
        preMakespan = self.getPredictMakespan(humID,predictEndProTime)

        
#        print(preMakespan)
#        print(arrTime)
        
        predictProDur = preMakespan - arrTime
        
        
#        print(preMakespan)
#        print(arrTime)
        
        if predictWorkLoad > 0 and predictWorkLoad < 7:
            workRate  = self._inWorkEffZone        
        else:
            if predictWorkLoad <=10:                
                workRate = self._outWorkEffZone
            else:
                workRate = self._beyondWorkZone                      

        if predictWorkLoad <= 0:
            raise Exception()
                    
        if self._allianceID[robID] == humID:
            allRate = self._inAllRate
        else:
            allRate = self._outAllRate
            
        return workRate*allRate/predictProDur,predictEndProTime,predictProTime

    
    




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
    