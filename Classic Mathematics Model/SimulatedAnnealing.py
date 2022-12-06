"""
@Author: Ansehen
@Date: 2022.Jan.29th
Simulated Annealing
"""
from abc import abstractmethod
import math
import random


class SimulatedAnnealing(object):
    def __init__(self, T_init: float, T_min: float, time: int, up_bnd: int, low_bnd: int):
        """
        T_init: initiate temperature
        T_min: minimum temperature
        time: time for whole iter
        up_bnd: Maximum Boundary of the input data
        low_bnd: Minimum Boundary of the input data
        """
        self.T_init = T_init
        self.T_min = T_min
        self.time = time
        self.up_bnd, self.low_bnd = up_bnd, low_bnd

    def simulating(self, function, x, method='accelerate'):
        # TODO: Loss Function Purpose
        # while condition_evaluate(self.purpose(xxxxx)):
        while self.T_init >= self.T_min:
            for _ in range(self.time):
                # calculate res
                res = function(x)
                # generate a new x in the neighborhood of x by transform function
                x_new = x + random.uniform(-0.055, 0.055) * self.T_init
                if self.low_bnd <= x_new <= self.up_bnd:
                    res_new = function(x_new)
                    if res_new - res < 0:
                        x = x_new
                    else:
                        # metropolis principle
                        probability = math.exp(-(res_new-res)/self.T_init)
                        r = random.uniform(0, 1)
                        if r < probability:
                            x = x_new
                else:
                    print('x is overflow the definition interval!')
                    break
            else:
                print('One Time Totally Done!')
            self.time += 1
            if method == "classic":
                self.T_init = 1000/math.log(1+self.time)
            elif method == "accelerate":
                self.T_init = 1000/(1+self.time)
            else:
                raise TypeError('Method with Wrong Implementation!')
            print("Results for epoch{}--> function res:{}, x={}".format(self.time, function(x), x))

    @abstractmethod
    def purpose(self, function, *args):
        # TODO: Loss function definition
        return NotImplemented


if __name__ == '__main__':
    def function(x):
        return x**3-60*x**2-4*x+6

    T_init, T_min, time, up_bnd, low_bnd = 1000, 10, 0, 100, 0
    x = random.uniform(0, 100)
    model = SimulatedAnnealing(T_init, T_min, time, up_bnd, low_bnd)
    model.simulating(function=function, x=x)
