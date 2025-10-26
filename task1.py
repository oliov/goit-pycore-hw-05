def caching_fibonacci():
    cache = {}
    def fibonacci(num):
        if num <= 0: return 0
        if num == 1: return 1 
        if num in cache: return cache[num]

        cache[num] = fibonacci(num - 1) + fibonacci(num - 2)
        return cache[num]
    return fibonacci


# Отримуємо функцію fibonacci
fib = caching_fibonacci()
int_: int = 'str'
# Використовуємо функцію fibonacci для обчислення чисел Фібоначчі
print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610
