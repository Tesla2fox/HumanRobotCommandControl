# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:08:35 2019

ggq 创建的human 模型 
@author: robot
"""

#import numpy

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from Robot import TaskType
import Robot



from enum import Enum

class disType(Enum):
    normal = 0
    formal = 1
    
class ControlMode(Enum):
    MBC = 0
    MBE = 1





'''
各种模型假设
'''

class HumanModel(object):
    def __init__(self):
        '''
        集结和搜索的 processTime 服从正态分布                
        '''
        self.a_time_disType = disType.normal
        self.s_time_disType = disType.normal
        self.a_timeProcess_mu = 2
        self.a_timeProcess_sigma = 0.5
        '''
        集结和搜索的 processTime 服从正态分布                
        '''
        self.a_time_disType = disType.normal
        self.s_time_disType = disType.normal
        self.a_timeProcess_mu = 2
        self.a_timeProcess_sigma = 0.5        
        
        self._max_workLoad = 10
        
    def getWorkEfficieny(self,c_workload,c_fatigue):
        '''
        maxWorkEff = 1.5
        normalWorkEff = 1
        minWorkEff = 0.2
        最优工作效率区间是 0 - 8.15
        '''        
        if c_workload < self._max_workLoad*0.5:
            workEff = 1
        else:
            if c_workload < self._max_workLoad * 0.7:                
                workEff  = 0.5/(0.2*self._max_workLoad) * (c_workload - 0.5* self._max_workLoad) + 1
            else:
                if c_workload < self._max_workLoad:                    
                    workEff = -1.3/(0.3*self._max_workLoad)* (c_workload - 0.7* self._max_workLoad) + 1.5
                else:
                    workEff = 0.2        
        if c_fatigue > 100:
            workEff =  workEff*0.5
        return workEff
    
    def getProcessTime(self,_workEff,_taskType):
        print('_taskType',_taskType)
        if _taskType == TaskType.Aggregation:
           workQuantity = np.random.uniform(1,2)
           proTime = workQuantity/_workEff
        if _taskType == TaskType.Surveillance:
           workQuantity = np.random.normal(2,0.5)           
           proTime = workQuantity/_workEff
        print(proTime)
        return proTime
    def getPredictProcessTime(self,_workEff,_taskType):
        if _taskType == TaskType.Aggregation:
           workQuantity = 1.5
           proTime = workQuantity/_workEff
        if _taskType == TaskType.Surveillance:
           workQuantity = 2           
           proTime = workQuantity/_workEff
        return proTime
            
    def getWorkLoad(self,_taskType):
        if _taskType == TaskType.Aggregation:
            _workLoad = 2
        if _taskType == TaskType.Surveillance:
            _workLoad = 3
        return _workLoad

class Human(HumanModel):
    def __init__(self,index):
        super(Human,self).__init__()
        self._index = index
        self._cWorkLoad = 0
        self._cFatigue = 0
        self._cRobLst = []
    def __str__(self):
        return 'Hum index =  ' + str(self._index)
        
        pass
    

    
import numpy as np    
    
if __name__ == '__main__':
        
    test_model = HumanModel()
    print(test_model.getWorkEfficieny(11,20))
#    print(np.random.choice(4,15))
##    f = open('')        
#    f = open('pyCfg.dat','w')    
#    for i in range(3):
#        f.write('index ' + str(i))
#        f.write(' fireRocket ')
#        f.write(' dis ' + str(disType.formal) + ' 0 ')
#        f.write(' low ' + str(3) + '  high '+ str(5))
#        f.write('\n')
#    for i in range(3,6):
#        f.write('index ' + str(i))
#        f.write(' dubinsScoutCar ')
#        f.write(' dis ' + str(disType.formal) + ' 0 ')
#        f.write(' low ' + str(4) + '  high '+ str(6))
#        f.write('\n')
#        
#    for i in range(7,9):
#        f.write('index ' + str(i))
#        f.write(' no_dubinsScoutCar ')
#        f.write(' dis ' + str(disType.formal) + ' 0 ')
#        f.write(' low ' + str(3) + '  high '+ str(5))
#        f.write('\n')        
#
#    for i in range(10,12):
#        f.write('index ' + str(i))
#        f.write(' fireGuard ')
#        f.write(' dis ' + str(disType.formal) + ' 0 ')
#        f.write(' low ' + str(3) + '  high '+ str(5))
#        f.write('\n')        
#
#    for i in range(7,9):
#        f.write('index ' + str(i))
#        f.write(' no_dubinsCar ')
#        f.write(' dis ' + str(disType.formal) + ' 0 ')
#        f.write(' low ' + str(3) + '  high '+ str(5))
#        f.write('\n')        
#        
#    for i in range(15):
#        f.write('wtf\n')
#    f.close()
#    print(disType(1))
#
