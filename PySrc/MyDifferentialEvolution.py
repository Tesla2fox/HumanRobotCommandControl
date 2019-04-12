# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 09:51:17 2019

@author: robot
"""

from scipy.optimize import differential_evolution
from scipy.optimize._differentialevolution import DifferentialEvolutionSolver


from scipy.optimize import OptimizeResult, minimize
from scipy.optimize.optimize import _status_message
from scipy._lib.six import xrange, string_types


import numpy as np



'''
some libs for drawing 
'''

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import plotly.io as pio


def my_differential_evolution(func, bounds, args=(), strategy='best1bin',
                           maxiter=1000, popsize=15, tol=0.01,
                           mutation=(0.5, 1), recombination=0.7, seed=None,
                           callback=None, disp=False, polish=True,
                           init='latinhypercube', atol=0,drawPlotBool = False):
    
    solver = MyDifferentialEvolutionSolver(func, bounds, args=args,
                                         strategy=strategy, maxiter=maxiter,
                                         popsize=popsize, tol=tol,
                                         mutation=mutation,
                                         recombination=recombination,
                                         seed=seed, polish=polish,
                                         callback=callback,
                                         disp=disp, init=init, atol=atol, drawPlotBool = drawPlotBool)
    res = solver.solve()
    if drawPlotBool:
        solver.drawPlot()
    return res
    
class MyDifferentialEvolutionSolver(DifferentialEvolutionSolver):
    def __init__(self, func, bounds, args=(),
                 strategy='best1bin', maxiter=1000, popsize=15,
                 tol=0.01, mutation=(0.5, 1), recombination=0.7, seed=None,
                 maxfun=np.inf, callback=None, disp=False, polish=True,
                 init='latinhypercube', atol=0, drawPlotBool = False):
        super(MyDifferentialEvolutionSolver,self).__init__(func, bounds, args=(),
                 strategy='best1bin', maxiter=1000, popsize=15,
                 tol=0.01, mutation=(0.5, 1), recombination=0.7, seed=None,
                 maxfun=np.inf, callback=None, disp=False, polish=True,
                 init='latinhypercube', atol=0)
        self.drawPlotBool = drawPlotBool
        self.drawX = []
        self.drawY = []
        pass
    
    def solve(self):
        """
        Runs the DifferentialEvolutionSolver.

        Returns
        -------
        res : OptimizeResult
            The optimization result represented as a ``OptimizeResult`` object.
            Important attributes are: ``x`` the solution array, ``success`` a
            Boolean flag indicating if the optimizer exited successfully and
            ``message`` which describes the cause of the termination. See
            `OptimizeResult` for a description of other attributes.  If `polish`
            was employed, and a lower minimum was obtained by the polishing,
            then OptimizeResult also contains the ``jac`` attribute.
        """
        nit, warning_flag = 0, False
        status_message = _status_message['success']

        # The population may have just been initialized (all entries are
        # np.inf). If it has you have to calculate the initial energies.
        # Although this is also done in the evolve generator it's possible
        # that someone can set maxiter=0, at which point we still want the
        # initial energies to be calculated (the following loop isn't run).
        if np.all(np.isinf(self.population_energies)):
            self._calculate_population_energies()

        # do the optimisation.
        for nit in xrange(1, self.maxiter + 1):
            # evolve the population by a generation
            try:
                next(self)
            except StopIteration:
                warning_flag = True
                status_message = _status_message['maxfev']
                break

            if self.disp:
                print("differential_evolution step %d: f(x)= %g"
                      % (nit,
                         self.population_energies[0]))
            if self.drawPlotBool:
                self.drawX.append(nit)
                self.drawY.append(self.population_energies[0])
            # should the solver terminate?
            convergence = self.convergence

            if (self.callback and
                    self.callback(self._scale_parameters(self.population[0]),
                                  convergence=self.tol / convergence) is True):

                warning_flag = True
                status_message = ('callback function requested stop early '
                                  'by returning True')
                break

            intol = (np.std(self.population_energies) <=
                     self.atol +
                     self.tol * np.abs(np.mean(self.population_energies)))
            if warning_flag or intol:
                break

        else:
            status_message = _status_message['maxiter']
            warning_flag = True

        DE_result = OptimizeResult(
            x=self.x,
            fun=self.population_energies[0],
            nfev=self._nfev,
            nit=nit,
            message=status_message,
            success=(warning_flag is not True))

        if self.polish:
            result = minimize(self.func,
                              np.copy(DE_result.x),
                              method='L-BFGS-B',
                              bounds=self.limits.T,
                              args=self.args)

            self._nfev += result.nfev
            DE_result.nfev = self._nfev

            if result.fun < DE_result.fun:
                DE_result.fun = result.fun
                DE_result.x = result.x
                DE_result.jac = result.jac
                # to keep internal state consistent
                self.population_energies[0] = result.fun
                self.population[0] = self._unscale_parameters(result.x)

        return DE_result

    def drawPlot(self):
        trace = go.Scatter(mode = 'lines+markers',
                            x = self.drawX,
                            y = self.drawY,
                            name = 'DE_cruve')
        figData = [trace]
        fig = go.Figure(data = figData)
#        pio.write_image(fig,'De_cruve.pdf')
        plotly.offline.plot(fig,filename = 'De_cruve.html',validate=False)



if __name__ == '__main__':
    def ackley(x):
        arg1 = -0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))
        arg2 = 0.5 * (np.cos(2. * np.pi * x[0]) + np.cos(2. * np.pi * x[1]))
        return -20. * np.exp(arg1) - np.exp(arg2) + 20. + np.e
    bounds = [(-5, 5), (-5, 5)]
    result = my_differential_evolution(ackley, bounds, disp = True, drawPlotBool = True)

    print(result)

