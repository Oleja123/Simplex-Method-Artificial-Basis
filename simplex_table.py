import numpy as np


class SimplexTable:

    def __init__(self, n, m, f, a, b):

        self.n = n
        self.m = m
        self.a = [[0 for j in range(m)] for i in range(n + m)]
    #предобрабатываю данные, чтоб удобнее потом перемножать было
        for i in range(len(a)):
            for j in range(len(a[i])):
                self.a[j][i] = a[i][j]
        
        for i in range(m):
            self.a[n + i][i] = 1
    #элемент базиса храню как тапл вида (номер переменной, значение, домноженно ли до m)
        self.basis = [(n + i, 1, 1) for i in range(m)]
    #схожим образом храню коэффициенты в целевой функции
        self.f = [(f[i], 0) for i in range(n)]
        self.f += [(1, 1) for i in range(m)]
    #значения моих оценок для каждого столбца с m и без нее
        self.score = [0 for i in range(n + m)]
        self.score_m = [0 for i in range(n + m)]
    #текущие значения правых сторон ограничений
        self.a0 = b
        self._update_score()
    
    def _update_score(self): #функция для пересчета оценок для столбцов

        self.score = [0 for i in range(len(self.score))]
        self.score_m = [0 for i in range(len(self.score_m))]
        for i in range(self.n + self.m):
            for j in range(self.m):
                res = self.a[i][j] * self.basis[j][1]
                print(res)
                if self.basis[j][2] == 0:
                    self.score[i] += res
                else:
                    self.score_m[i] += res
            if self.f[i][1] == 0:
                self.score[i] -= self.f[i][0]
            else:
                self.score_m[i] -= self.f[i][0]

    def print_table_info(self):
        for i in range(self.n + self.m):
            print(*self.a[i])
        print(*self.basis)
        print(*self.f)
        print(*self.a0)
        print(*self.score)
        print(*self.score_m)