import numpy as np
import matplotlib.pyplot as plt


class ACO(object):
    def __init__(self, parameters):
        # Initiate
        # iteration
        self.NGEN = parameters[0]
        # 种群大小
        self.pop_size = parameters[1]
        # 变量个数
        self.var_num = len(parameters[2])
        self.bound = []  # 变量的约束范围
        self.bound.append(parameters[2])
        self.bound.append(parameters[3])

        self.pop_x = np.zeros((self.pop_size, self.var_num))  # 所有蚂蚁的位置
        self.g_best = np.zeros((1, self.var_num))  # 全局蚂蚁最优的位置

        # 初始化第0代初始全局最优解
        temp = -1
        for i in range(self.pop_size):
            for j in range(self.var_num):
                self.pop_x[i][j] = np.random.uniform(self.bound[0][j], self.bound[1][j])
            fit = self.fitness(self.pop_x[i])
            if fit > temp:
                self.g_best = self.pop_x[i]
                temp = fit

    def fitness(self, ind_var):
        x1 = ind_var[0]
        x2 = ind_var[1]
        x3 = ind_var[2]
        x4 = ind_var[3]
        return x1**2 + x2**2 - x3**2 + x4**2

    def update_operator(self, gen, t, t_max):
        rou = 0.8  # 信息素挥发系数
        Q = 1  # 信息释放总量
        lamda = 1 / gen
        pi = np.zeros(self.pop_size)
        for i in range(self.pop_size):
            for j in range(self.var_num):
                pi[i] = (t_max - t[i]) / t_max
                # 更新位置
                if pi[i] < np.random.uniform(0, 1):
                    self.pop_x[i][j] = self.pop_x[i][j] + np.random.uniform(-1, 1) * lamda
                else:
                    self.pop_x[i][j] = self.pop_x[i][j] + np.random.uniform(-1, 1) * (
                            self.bound[1][j] - self.bound[0][j]) / 2
                # 越界保护
                if self.pop_x[i][j] < self.bound[0][j]:
                    self.pop_x[i][j] = self.bound[0][j]
                if self.pop_x[i][j] > self.bound[1][j]:
                    self.pop_x[i][j] = self.bound[1][j]
            # 更新t值
            t[i] = (1 - rou) * t[i] + Q * self.fitness(self.pop_x[i])
            # 更新全局最优值
            if self.fitness(self.pop_x[i]) > self.fitness(self.g_best):
                self.g_best = self.pop_x[i]
        t_max = np.max(t)
        return t_max, t

    def main(self):
        popobj = []
        best = np.zeros((1, self.var_num))[0]
        for gen in range(1, self.NGEN + 1):
            if gen == 1:
                tmax, t = self.update_operator(gen, np.array(list(map(self.fitness, self.pop_x))),
                                               np.max(np.array(list(map(self.fitness, self.pop_x)))))
            else:
                tmax, t = self.update_operator(gen, t, tmax)
            popobj.append(self.fitness(self.g_best))
            print('############ Generation {} ############'.format(str(gen)))
            print(self.g_best)
            print(self.fitness(self.g_best))
            if self.fitness(self.g_best) > self.fitness(best):
                best = self.g_best.copy()
            print('最好的位置：{}'.format(best))
            print('最大的函数值：{}'.format(self.fitness(best)))
        print("---- End of (successful) Searching ----")

        plt.figure()
        plt.title("Figure1")
        plt.xlabel("iterators", size=14)
        plt.ylabel("fitness", size=14)
        t = [t for t in range(1, self.NGEN + 1)]
        plt.plot(t, popobj, color='b', linewidth=2)
        plt.show()


if __name__ == '__main__':
    NGEN = 100
    popsize = 100
    low = [1, 1, 1, 1]
    up = [30, 30, 30, 30]
    parameters = [NGEN, popsize, low, up]
    aco = ACO(parameters)
    aco.main()