

"""
Closure (闭包)
1. 闭包 = 函数 + 它定义时所捕获的外部变量环境

3. 闭包的三个必要条件：
- 存在嵌套函数
- 内部函数引用了外部函数的变量
- 外部函数返回内部函数
"""

def outer(x):
    _x = 1
    def inner(y):
        return _x + y**2 - x
    return inner

f = outer(10)
print(f"此时这里的f是带上了_x=1和x=10: {f(0)}")
print("="*20)
print(f.__closure__)  # 查看闭包捕获的单元格对象
print(f.__code__.co_freevars)  # ('_x', 'x') - 自由变量名
print("="*20)
print(f"可以看到f为一个函数: {f}")
print(f(5))
print("="*20)

# 作用1：轻量私有变量
def counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = counter()
for _ in range(2):
    print(c())
print("="*20)

# 作用二工厂函数
def multiply(x):
    return lambda y: x * y

double = multiply(2)
print(double(12.2))