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
    #элемент базиса храню как тапл вида (номер переменной, значение, домноженно ли до M)
        self.basis = [(n + i, 1, 1) for i in range(m)]
    #схожим образом храню коэффициенты в целевой функции (значеник, домноженно ли на M)
        self.f = [(f[i], 0) for i in range(n)]
        self.f += [(1, 1) for i in range(m)]
    #значения моих оценок для каждого столбца с m и без нее
        self.score = [0 for i in range(n + m)]
        self.score_m = [0 for i in range(n + m)]
    #текущие значения правых сторон ограничений
        self.b = b
        self._update_score()
    
    def _update_score(self): #функция для пересчета оценок для столбцов

        self.score = [0 for i in range(len(self.score))]
        self.score_m = [0 for i in range(len(self.score_m))]
        for i in range(self.n + self.m):
            for j in range(self.m):
                res = self.a[i][j] * self.basis[j][1]
                if self.basis[j][2] == 0:
                    self.score[i] += res
                else:
                    self.score_m[i] += res
            if self.f[i][1] == 0:
                self.score[i] -= self.f[i][0]
            else:
                self.score_m[i] -= self.f[i][0]

    def _check_is_optimal_phase1(self): #функция для проверки того, что фаза 1 закончилась
        for i in self.score_m:
            if self.score_m > 0:
                return False
        return True

    def _relax_table(self, sz, f): #функция для ввода вектора, соответствующего максимуму, в базис
        current_max = 0
        current_min = 0
        max_ind = -1
        min_ind = -1
        for i in range(sz):
            if f[i] > current_max:
                max_ind = i
                current_max = f[i]
        for i in range(len(self.a[max_ind])):
            if self.b[i] / self.a[max_ind][i] < current_min or min_ind == -1:
                current_min = self.b[i] / self.a[max_ind][i]
                min_ind = i
        for i in range(self.m): #релаксируем столбец b
            if i != min_ind:
                self.b[i] = self.b[i] - (self.b[min_ind] / self.a[max_ind][min_ind]) * self.a[max_ind][i]
            else:
                self.b[i] = self.b[min_ind] / self.a[max_ind][min_ind]
        tmp = [[0 for j in range(len(self.a[i]))] for i in range(len(self.a))]
        for i in range(sz): #релаксируем матрицу
            for j in range(len(self.a[i])):
                if j == min_ind:
                    tmp[i][j] = self.a[i][j] / self.a[max_ind][min_ind]
                else:
                    tmp[i][j] = self.a[i][j] - self.a[i][min_ind] / self.a[max_ind][min_ind] * self.a[max_ind][j]
        self.a = tmp
        self.basis[min_ind] = (max_ind, *self.f[max_ind])
        self._update_score()

    def phase1(self):
        # while self.check_is_optimal_phase1():
            self._relax_table(self.n + self.m, self.score_m)

    def print_table_info(self):
        for i in range(self.n + self.m):
            print(*self.a[i])
        print(*self.basis)
        print(*self.f)
        print(*self.b)
        print(*self.score)
        print(*self.score_m)