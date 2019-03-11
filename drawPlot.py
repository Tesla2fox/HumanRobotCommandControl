# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:36:06 2019

@author: robot
"""







import plotly.plotly as py
import plotly.figure_factory as ff
import plotly

py.sign_in('tesla_fox', 'HOTRQ3nIOdYUUszDIfgN')

#df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
#      dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
#      dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')]
#
#fig = ff.create_gantt(df)
#py.iplot(fig, filename='gantt-simple-gantt-chart', world_readable=True)

#import plotly.plotly as py
#import plotly.figure_factory as ff


df = [dict(Task='Agent-0', Start='1', Finish='4', Resource='Complete'),
      dict(Task="Job-1", Start='2', Finish='3', Resource='Incomplete'),
      dict(Task="Job-2", Start='3', Finish='2', Resource='Not Started'),
      dict(Task="Job-2", Start='4', Finish='9', Resource='Complete'),
      dict(Task="Job-3", Start='5', Finish='2017-03-20', Resource='Not Started'),
      dict(Task="Job-3", Start='1', Finish='2017-04-20', Resource='Not Started'),
      dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
      dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')
      ]

colors = {'Not Started': 'rgb(220, 0, 0)',
          'Incomplete': (1, 0.9, 0.16),
          'Complete': 'rgb(0, 255, 100)'}

fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)

fig['layout']['xaxis']['type'] = 'linear'

plotly.offline.plot(fig, filename='gantt-group-tasks-together')