class Metrix:
    def __init__(self, ls):
        self.body: list[list] = ls
        self.n = len(ls)

    def det(self):
        if self.n == 2:
            return self.__det2()
        else:
            sum = 0
            for j, a in enumerate(self.body[0]):
                mtx = self.body[1:]
                mtx = Metrix([ls[:j] + ls[j + 1:] for ls in mtx])
                sum += (-1) ** (2 + j) * mtx.det() * a
            return sum

    def __det2(self):
        return self.body[0][0] * self.body[1][1] - self.body[0][1] * self.body[1][0]

    def __mul__(self, other: any):
        if isinstance(other, (int, float)):
            mtx = []
            for i in self.body:
                mtx.append([j * other for j in i])
            return Metrix(mtx)
        elif isinstance(other, Vector):
            ls = []
            for i in range(self.n):
                ls.append([self.body[i][j] * other.ls[j] for j in range(self.n)])
            return Vector(ls)
        else:
            raise TypeError

    def cofactor(self):
        mtx = []
        for i in range(self.n):
            mtx.append([self.__minor(i, j) * (-1) ** (j + i) for j in range(self.n)])
        return Metrix(mtx)

    def transpose(self):
        mtx = []
        for j in range(self.n):
            mtx.append([self.body[i][j] for i in range(self.n)])
        return Metrix(mtx)

    def __minor(self, i, j):
        mtx = self.body[:i] + self.body[i + 1:]
        mtx = Metrix([ls[:j] + ls[j + 1:] for ls in mtx])
        return mtx.det()

    def inverse(self):
        s = self.det()
        if s == 0:
            print("Can't inverse the metrix")
            return None
        else:
            s = 1 / s
            mtx = self.cofactor().transpose()
            return mtx * s


class Vector:
    def __init__(self, ls):
        self.ls = ls
        self.n = len(ls)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i * other for i in self.ls])
        elif isinstance(other, Vector):
            return Vector([i * j for i, j in zip(self.ls, other.ls)])
        elif isinstance(other, Metrix):
            ls = []
            for i in range(self.n):
                ls.append(sum([other.body[i][j] * self.ls[j] for j in range(self.n)]))
            return Vector(ls)
        else:
            raise TypeError


class Regression:
    def __init__(self):
        self.func = None

    def poly(self, x: list[int | float], y: list[int | float], m: int) -> None:
        if m == 1:
            x_y = [xi * yi for xi, yi in zip(x, y)]
            x_s = [xi ** 2 for xi in x]
            y_avg = sum(y) / len(y)
            x_avg = sum(x) / len(x)
            a = (sum(x_y) - x_avg * y_avg) / (sum(x_s) - x_avg ** 2)
            b = y_avg - a * x_avg
            self.func = lambda x: a * x + b
        else:
            mtx = []
            for i in range(m + 1):
                ls = []
                for j in range(m + 1):
                    ls.append(sum([xi ** (i + j) for xi in x]))
                mtx.append(ls)
            print(f"mtx: {mtx}")
            mtx = Metrix(mtx).inverse()
            print(f"mtx inv: {mtx.body}")
            ls = []
            for i in range(m + 1):
                ls.append(sum([yi * xi ** i for xi, yi in zip(x, y)]))
            print(ls)
            vec = Vector(ls)
            coef = vec * mtx
            print("c:", coef.ls)

            def f(x):
                return sum([c * x ** i for i, c in enumerate(coef.ls)])

            print(f)
            print(f(1))
            self.func = f

    def val(self, x):
        if self.func is None:
            print("the regression was not yet fitted")
        else:
            return [self.func(xi) for xi in x]

    def score(self, y, y_val):
        mean = sum(y) / len(y)
        ssr = sum([(yi - yi_val) ** 2 for yi, yi_val in zip(y, y_val)])
        sst = sum([(yi - mean) ** 2 for yi in y])
        return 1 - (ssr / sst)