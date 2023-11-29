import numpy as np


class LinearComparison:
    def __init__(self) -> None:
        self.period = 1
        self.result = np.array([])
        self.m = None
        self.a = None
        self.c = None
        self.x = None
        self.n = None

    def update(self, m, a, c, x, n):
        self.m = m
        self.a = a
        self.c = c
        self.x = x
        self.n = n

    def gen_list(self) -> np.ndarray:
        if not self.result.size:
            self.result = np.empty(self.n, dtype=np.uint64)

        for i in range(self.n):
            self.x = (self.a * self.x + self.c) % self.m
            self.result[i] = self.x
        return self.result.tolist()

    def find_period(self) -> int:
        for i in range(1, len(self.result)):
            if self.result[i] == self.result[0]:
                break
            else:
                self.period += 1
        return self.period





