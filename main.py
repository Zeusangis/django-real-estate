L = (6, -3, -6, 10, 10, 0, -9, 0, 0.5, 2, 0, -7, -9, 5, 0, 0, -6, 0)
sum = 0
for num in L:
    sum = sum + num
print(sum)
print("The type of the result is ", type(sum).__name__)

M = list(L)
M = M[:-4]
print(M)
