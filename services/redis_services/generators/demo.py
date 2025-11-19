def demo():
    try:
        for i in range(10):
            print(i)
            yield i
    finally:
        print('yes')

p = demo()
next(p)
next(p)
next(p)
print(p)
for i in p:
    print(i, end="")
