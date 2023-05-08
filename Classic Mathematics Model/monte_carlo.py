import numpy as np


class MonteCarlo(object):
    def __init__(self, rand_points):
        self.rand_points = rand_points

    def calculate(self, condition):
        get_p = 0
        for i in range(self.rand_points):
            get_p += condition(index=i)
        else:
            print('Pipeline Ended!')
        return condition(res_stat=get_p)


def func1(index=None, res_stat=None):
    """
    index: index indicator in iterator
    res_stat: result func results
    return: condition or calculate result
    t/m=pi/4
    """
    if res_stat is not None:
        return 4 * res_stat / m
    if index is not None:
        if (x[index]-0.5)**2+(y[index]-0.5)**2 <= 1/4:
            return 1
        else:
            return 0


def func2(index=None, res_stat=None):
    if res_stat is not None:
        return 4 * res_stat / m
    if index is not None:
        if y[index] <= x[index]**2:
            return 1
        else:
            return 0


if __name__ == '__main__':
    # Demo 1
    m = 10**6
    x = np.random.random(m)
    y = np.random.random(m)
    MC = MonteCarlo(m)
    fin = MC.calculate(func1)
    print(fin)

    # Demo 2
    x = x+1
    y = 4*y
    fin2 = MC.calculate(func2)
    print(fin2)