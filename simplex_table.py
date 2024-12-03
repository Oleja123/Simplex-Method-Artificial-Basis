from no_solution_error import NoSolutionError
from miscalc_number import MiscalcNumber as ms


class SimplexTable:

    def __init__(self, n, m, f, a, b):

        self.n = n
        self.m = m
        self.ina = a
        self.inb = b
        self.a = [[ms(0) for j in range(m)] for i in range(n + m)]
    # предобрабатываю данные, чтоб удобнее потом перемножать было
        for i in range(len(a)):
            for j in range(len(a[i])):
                self.a[j][i] = ms(a[i][j])

        for i in range(m):
            self.a[n + i][i] = ms(1)
    # элемент базиса храню как тапл вида (номер переменной, значение, домноженно ли до M)
        self.basis = [(n + i, ms(1), 1) for i in range(m)]
    # схожим образом храню коэффициенты в целевой функции (значеник, домноженно ли на M)
        self.f = [(ms(f[i]), 0) for i in range(n)]
        self.f += [(ms(1), 1) for i in range(m)]
    # значения моих оценок для каждого столбца с m и без нее
        self.score = [ms(0) for i in range(n + m)]
        self.score_m = [ms(0) for i in range(n + m)]
    # текущие значения правых сторон ограничений
        self.b = [ms(i) for i in b]
        self._update_score(self.n + self.m)

    def solve(self):
        self._phase1()
        self._phase2()

    def _update_score(self, sz):  # функция для пересчета оценок для столбцов

        self.score = [ms(0) for i in range(len(self.score))]
        self.score_m = [ms(0) for i in range(len(self.score_m))]
        for i in range(sz):
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

    # функция для проверки того, что фаза
    def _check_is_optimal_phase(self, f):
        for i in f:
            if i.number > 0:
                return False
        return True

    # функция для ввода вектора, соответствующего максимуму, в базис
    def _relax_table(self, sz, f):
        current_max = 0
        current_min = 0
        max_ind = -1
        min_ind = -1
        for i in range(sz):
            if f[i].number > current_max:
                max_ind = i
                current_max = f[i].number
        for i in range(len(self.a[max_ind])):
            if self.a[max_ind][i].number > 0 and ((self.b[i] / self.a[max_ind][i]).number < current_min or min_ind == -1):
                current_min = (self.b[i] / self.a[max_ind][i]).number
                min_ind = i
        if min_ind == -1:
            raise NoSolutionError('Решения нет, целевая функция неограичена')
        b_tmp = [ms(0) for i in range(len(self.b))]
        for i in range(self.m):  # релаксируем столбец b
            if i != min_ind:
                b_tmp[i] = self.b[i] - (self.b[min_ind] /
                                        self.a[max_ind][min_ind]) * self.a[max_ind][i]
            else:
                b_tmp[i] = self.b[min_ind] / self.a[max_ind][min_ind]
        self.b = b_tmp
        tmp = [[ms(0) for j in range(len(self.a[i]))] for i in range(len(self.a))]
        for i in range(sz):  # релаксируем матрицу
            for j in range(len(self.a[i])):
                if j == min_ind:
                    tmp[i][j] = self.a[i][j] / self.a[max_ind][min_ind]
                else:
                    tmp[i][j] = self.a[i][j] - self.a[i][min_ind] / \
                        self.a[max_ind][min_ind] * self.a[max_ind][j]
        self.a = tmp
        self.basis[min_ind] = (max_ind, *self.f[max_ind])
        self._update_score(sz)

    def _phase1(self):
        while not self._check_is_optimal_phase(self.score_m):
            self._relax_table(self.n + self.m, self.score_m)
        for i in self.basis:
            if i[0] >= self.n:
                raise NoSolutionError(
                    'Решения нет, в базисе получились искусственные переменные')

    def _phase2(self):
        self.a = self.a[:self.n]
        self.score = self.score[:self.n]
        self.f = self.f[:self.n]
        while not self._check_is_optimal_phase(self.score):
            self._relax_table(self.n, self.score)

    def get_ans(self):
        ans = ms(0)
        for j in range(self.m):
            ans += self.b[j] * self.basis[j][1]
        return ans

    def print_table_info(self):
        vals = [-1 for i in range(self.n)]
        for i in range(self.m):
            vals[self.basis[i][0]] = self.b[i].number
        print(*vals)
        for i in range(self.m):
            ind = -1
            mn = -1
            curb = self.inb[i]
            for j in range(self.n):
                print(i, j, self.ina[i][j], vals[j])
                if self.ina[i][j] != 0 and vals[j] == -1:
                    ind = j
                    mn = self.ina[i][j]
                else:
                    curb -= vals[j] * self.ina[i][j]
            if ind != -1:
                vals[ind] = curb / mn
        for i in range(self.n):
            print('x' + str(i) + ' = ' + str(vals[i]))
        print(self.get_ans().number)