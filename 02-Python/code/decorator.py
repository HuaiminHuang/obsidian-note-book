import time

"""
Decorator装饰器
"""


# 无参数
def timer(func):
    def my_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"耗时: {(end - start):.4f}")
        return result

    return my_wrapper


@timer
def f():
    time.sleep(1.2)


# 带参数
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(5)
def g():
    print("Hello World!")


@repeat(2)
def h():
    print("=" * 20)


if __name__ == "__main__":
    f()  # 耗时: 1.2003
    print(f.__name__)
    h()
    g()
    print(g.__name__)
