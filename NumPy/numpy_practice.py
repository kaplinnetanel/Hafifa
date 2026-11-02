import numpy as np
from memory_profiler import profile

# numbers = np.array([[10,20,30],[40,50,60]])



# print(numbers.shape)
# print(numbers.ndim)
# print(numbers.size)
# print(numbers.shape)



# def creat_numbers():
#     numbers = (i for i in range(10000))
#     yield from numbers

# m = creat_numbers()
# print(next(m))

# print(next(m))
# print(next(m))
# print(next(m))


import timeit

a = timeit.timeit(
    "sum(range(1000))",
    number=10000
)

b = timeit.timeit(
    "sum([i for i in range(1000)])",
    number=10000
)

print("A:", a)
print("B:", b)