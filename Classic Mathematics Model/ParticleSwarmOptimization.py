"""
@Author: Ansehen
@Date: 2022.Jan.29th
Cellular automata
Reference: https://www.cxyzjd.com/article/qq_40875849/104688528
"""
import numpy as np
import random
import matplotlib.pyplot as plt


class PSO(object):
    def __init__(self, parameters):
        # initialize
        self.NGEN = parameters[0]   # generation
        self.pop_size = parameters[1]   # population size
        self.var_num = len(parameters[2])   # num of variables
        self.bound = []
        self.bound.append(parameters[2])
        self.bound.append(parameters[3])

        self.pop_x = np.zeros((self.pop_size, self.var_num))    # position of each particle
        self.pop_v = np.zeros((self.pop_size, self.var_num))    # velocity of each particle
        self.p_best = np.zeros((self.pop_size, self.var_num))   # optimize position of each particle
        self.g_best = np.zeros((1, self.var_num))   # global optimize position

        temp = -1
        for i in range(self.pop_size):
            for j in range(self.var_num):
                self.pop_x[i][j] = random.uniform(self.bound[0][j], self.bound[1][j])
                self.pop_v[i][j] = random.uniform(0, 1)
            self.p_best[i] = self.pop_x[i]      # save the most optimized individuals
            fit = self.fitness(self.p_best[i])
            if fit > temp:
                self.g_best = self.p_best[i]
                temp = fit

    def fitness(self, ind_var):
        x1 = ind_var[0]
        x2 = ind_var[1]
        x3 = ind_var[2]
        x4 = ind_var[3]
        y = x1 ** 2 + x2 ** 2 - x3 ** 3 + x4 ** 4
        return y

    def update_operator(self, pop_size):
        c1 = 2  # 学习因子，一般为2
        c2 = 2
        w = 0.4  # 自身权重因子
        for i in range(pop_size):
            # 更新速度
            self.pop_v[i] = w * self.pop_v[i] + c1 * random.uniform(0, 1) * (
                    self.p_best[i] - self.pop_x[i]) + c2 * random.uniform(0, 1) * (self.g_best - self.pop_x[i])
            # 更新位置
            self.pop_x[i] = self.pop_x[i] + self.pop_v[i]
            # 越界保护
            for j in range(self.var_num):
                if self.pop_x[i][j] < self.bound[0][j]:
                    self.pop_x[i][j] = self.bound[0][j]
                if self.pop_x[i][j] > self.bound[1][j]:
                    self.pop_x[i][j] = self.bound[1][j]
            # 更新p_best和g_best
            if self.fitness(self.pop_x[i]) > self.fitness(self.p_best[i]):
                self.p_best[i] = self.pop_x[i]
            if self.fitness(self.pop_x[i]) > self.fitness(self.g_best):
                self.g_best = self.pop_x[i]

    def main(self):
        popobj = []
        self.ng_best = np.zeros((1, self.var_num))[0]
        for gen in range(self.NGEN):
            self.update_operator(self.pop_size)
            popobj.append(self.fitness(self.g_best))
            print('############ Generation {} ############'.format(str(gen + 1)))
            if self.fitness(self.g_best) > self.fitness(self.ng_best):
                self.ng_best = self.g_best
            print('最好的位置：{}'.format(self.ng_best))
            print('最大的函数值：{}'.format(self.fitness(self.ng_best)))
        print("---- End of (successful) Searching ----")

        plt.figure()
        plt.title("Figure1")
        plt.xlabel("iterators", size=14)
        plt.ylabel("fitness", size=14)
        t = [t for t in range(self.NGEN)]
        plt.plot(t, popobj, color='b', linewidth=2)
        plt.show()


if __name__ == '__main__':
    NGEN = 100
    popsize = 100
    low = [1, 1, 1, 1]
    up = [30, 30, 30, 30]
    parameters = [NGEN, popsize, low, up]
    pso = PSO(parameters)
    pso.main()