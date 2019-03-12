# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 20:59:23 2018

@author: robot
"""

import plotly.plotly as py
import plotly.figure_factory as ff
import plotly


humNum = 4
humData_x = [[0] for i in range(humNum)]
humData_y = [[0] for i in range(humNum)]

print(humData_x)
print(humData_y)

df = []
with open('D:\\VScode\\HumanRobotCommandControl\\data//HRCC.dat') as txtData:
    lines = txtData.readlines()
    for line in lines:
        lineData = line.split()
        if (len(lineData)<= 1):
            continue
        else:
            if (lineData[0] == 'humID'):
                unitDic = dict(Task = 'hum' + lineData[1] , Start = lineData[5], Finish =  lineData[7],
                     Resource = 'rob' + lineData[3])
                df.append(unitDic) 
            if (lineData[0] == 'HumanWorkLoad'):
                humID = int(lineData[3])
                humData_x[humID].append(float(lineData[5]))
                humData_y[humID].append(float(lineData[1]))

import plotly.plotly as py
import plotly.graph_objs as go

scatter_data = []
for i in range(4):
    trace = go.Scatter(x = humData_x[i], y = humData_y[i],
               name = 'humWorkLoad' + str(i), mode = 'lines + markers', line = dict(shape = 'hv'))
    scatter_data.append(trace)
    
layout = dict(title = 'WorkLoad',
              yaxis = dict(zeroline = True),
              xaxis = dict(zeroline = True)
             )
fig = dict(data = scatter_data, layout=layout)
plotly.offline.plot(fig, filename='styled-scatter')

#for i                 
#                if lineData[3]
import colorlover as cl

#plotly.figure_factory


bupu = cl.scales['9']['div']['RdYlBu']
bupu15 = cl.interp(bupu, 150) # Map color scale to 500 bins
bupu15RGB = cl.to_rgb(bupu15) 

#print(bupu15)


dic = dict()
for i in range(15):
    dic['rob'+str(i)] = bupu15RGB[i*10]
    
import plotly.plotly as py
import plotly.figure_factory as ff
##
#df = [dict(Task = 'Human-0', Start = '0', Finish='4',Resource = 'rob0'),
#      dict(Task = 'Human-0', Start = '4', Finish='6',Resource = 'rob1')]

fig = ff.create_gantt(df,colors = dic ,index_col='Resource', show_colorbar=True, group_tasks=True)

#df = [dict(Task='Agent-0', Start='1', Finish='4', Resource='Complete'),
#      dict(Task="Job-1", Start='2', Finish='3', Resource='Incomplete'),
#      dict(Task="Job-2", Start='3', Finish='2', Resource='Not Started'),
#      dict(Task="Job-2", Start='4', Finish='9', Resource='Complete'),
##      dict(Task="Job-3", Start='5', Finish='2017-03-20', Resource='Not Started'),
##      dict(Task="Job-3", Start='1', Finish='2017-04-20', Resource='Not Started'),
##      dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
##      dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')
#      ]
#
#colors = {'Not Started': 'rgb(220, 0, 0)',
#          'Incomplete': (1, 0.9, 0.16),
#          'Complete': 'rgb(0, 255, 100)'}
#
#fig = ff.create_gantt(df, colors=dic, index_col='Resource', show_colorbar=True, group_tasks=True)

fig['layout']['xaxis']['type'] = 'linear'
fig['layout']['xaxis']['zeroline'] = True
#fig['layout']['yaxis']['zeroline'] = True


plotly.offline.plot(fig, filename='gantt-group-tasks-together')

#fig = ff.create_gantt(df)
#
##print(fig)
#fig['layout']['xaxis']['type'] = 'linear'
#
#plotly.offline.plot(fig, filename='gantt-simple-gantt-chart')
