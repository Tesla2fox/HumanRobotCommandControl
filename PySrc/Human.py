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
        pass


class Human(HumanModel):
    def __init__(self):
        pass

    
import numpy as np    
    
if __name__ == '__main__':
    print(np.random.choice(4,15))
#    f = open('')        
    f = open('pyCfg.dat','w')    
    for i in range(3):
        f.write('index ' + str(i))
        f.write(' fireRocket ')
        f.write(' dis ' + str(disType.formal) + ' 0 ')
        f.write(' low ' + str(3) + '  high '+ str(5))
        f.write('\n')
    for i in range(3,6):
        f.write('index ' + str(i))
        f.write(' dubinsScoutCar ')
        f.write(' dis ' + str(disType.formal) + ' 0 ')
        f.write(' low ' + str(4) + '  high '+ str(6))
        f.write('\n')
        
    for i in range(7,9):
        f.write('index ' + str(i))
        f.write(' no_dubinsScoutCar ')
        f.write(' dis ' + str(disType.formal) + ' 0 ')
        f.write(' low ' + str(3) + '  high '+ str(5))
        f.write('\n')        

    for i in range(10,12):
        f.write('index ' + str(i))
        f.write(' fireGuard ')
        f.write(' dis ' + str(disType.formal) + ' 0 ')
        f.write(' low ' + str(3) + '  high '+ str(5))
        f.write('\n')        

    for i in range(7,9):
        f.write('index ' + str(i))
        f.write(' no_dubinsCar ')
        f.write(' dis ' + str(disType.formal) + ' 0 ')
        f.write(' low ' + str(3) + '  high '+ str(5))
        f.write('\n')        
        
    for i in range(15):
        f.write('wtf\n')
    f.close()
    print(disType(1))

