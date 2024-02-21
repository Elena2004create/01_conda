for i in range(10000):
    d = i
    s = 0
    n = 0
    while s <= 365:
        s += d
        n += 5
    if n == 65:
        print(i)