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


#def demo1():

'''
各种模型假设
'''



class HumanModel(object):
    def __init__(self):
        '''
        processTime 服从正态分布
        
        
        '''
        self.a_timeProcess_mu = 2
        self.a_timeProcess_sigma = 0.5
        
        
        pass

    
if __name__ == '__main__':
    mu, sigma , num_bins = 0, 1, 50
    x = mu + sigma * np.random.randn(1000000)
    # 正态分布的数据
    n, bins, patches = plt.hist(x, num_bins, normed=True, facecolor = 'blue', alpha = 0.5)
    # 拟合曲线
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--')
    plt.xlabel('Expectation')
    plt.ylabel('Probability')
    plt.title('histogram of normal distribution: $\mu = 0$, $\sigma=1$')

    plt.subplots_adjust(left = 0.15)
    plt.show()
