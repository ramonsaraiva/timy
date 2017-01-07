# Timy

Minimalist measurement of python code time
> You can also use the built-in [timeit](https://docs.python.org/2.7/library/timeit.html) module

## Install
```
pip install timy
```

## Usage
Let's say you have a `calculate` function and you want to keep track of its execution time
```python
import timy

@timy.timer()
def calculate(n, r):
    """
    Divide, multiply and sum 'n' to every number in range 'r'
    returning the result list
    """
    return [i / n * n + n for i in range(r)]
```

Calling

```python
calculate(5, 10000000)
```

Output:

```
Timy executed (calculate) for 1 time(s) in 1.529540 seconds
Timy best time was 1.529540 seconds
```

Changing the **ident** and adding **loops** to the execution

```python
import timy

@timy.timer(ident='My calculation', loops=10)
def calculate(n, r):
    return [i / n * n + n for i in range(r)]
```

Output:

```
My calculation executed (calculate) for 10 time(s) in 15.165313 seconds
My calculation best time was 1.414186 seconds
```

Tracking **specific points** along your code

```python
import timy

with timy.Timer() as timer:
    N = 10000000
    for i in range(N):
        if i == N/2:
            timer.track('Half way')
```

Output:

```
Timy (Half way) 0.557577 seconds
Timy 0.988087 seconds
```

Another usage of tracking in a prime factors function

```python
def prime_factors(n):
    with timy.Timer('Factors') as timer:
        i = 2
        factors = []
        def add_factor(n):
            factors.append(n)
            timer.track('Found a factor')

        while i * i <= n:
            if n % i:
                i += 1
                continue
            n //= i
            add_factor(n)
        if n > 1:
            add_factor(n)
        return factors

factors = prime_factors(600851475143)
print(factors)
```

Output:

```
Factors (Found a factor) 0.000023 seconds
Factors (Found a factor) 0.000207 seconds
Factors (Found a factor) 0.000323 seconds
Factors (Found a factor) 0.000340 seconds
Factors 0.000349 seconds
[8462696833, 10086647, 6857, 6857]
```

## Contribute
Contributions are **always** welcome, but keep it simple and small.

## License
MIT
