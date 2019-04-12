# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:30:27 2019

@author: robot
"""

from enum import Enum

class TaskType(Enum):
    FireGuidance = 1
    FireAttack = 2
    Aggregation = 3
    Surveillance = 4
    Search = 5



class Robot(object):
    def __init__(self,index):
        self._index = index
        self._taskType = 0
        self._controlMode = 0
        self._humID = 0
        self._arrTime = 0
        self._beginProTime = 0
        self._endProTime = 0
        self._predictProTime = 0
        pass
    def __str__(self):
        return 'Rob index =  ' + str(self._index)


if __name__ == '__main__':
    rob = Robot(2)    
    print(rob)
    