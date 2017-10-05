# timy

![Python 3.3](https://img.shields.io/badge/python-3.3-blue.svg)
![Python 3.4](https://img.shields.io/badge/python-3.4-blue.svg)
![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)
![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)

![CircleCI](https://img.shields.io/circleci/project/github/ramonsaraiva/timy/master.svg)
![Codecov](https://img.shields.io/codecov/c/github/ramonsaraiva/timy/master.svg)

Minimalist measurement of python code time
> **timy** comes with a different idea of the built-in module [timeit](https://docs.python.org/2.7/library/timeit.html). It adds flexibility and different ways of measuring code time, using simple context managers and function decorators.

## Installing
```
pip install timy
```

## Usage

### Decorating a function
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

Whenever you call that function, the execution time will be tracked

```python
calculate(5, 10000000)
>> Timy executed (calculate) for 1 time(s) in 1.529540 seconds
>> Timy best time was 1.529540 seconds
```

Changing the **ident** and adding **loops** to the execution

```python
import timy

@timy.timer(ident='My calculation', loops=10)
def calculate(n, r):
    return [i / n * n + n for i in range(r)]
    
calculate(5, 10000000)
>> My calculation executed (calculate) for 10 time(s) in 15.165313 seconds
>> My calculation best time was 1.414186 seconds
```

### Tracking **specific points** along your code
The `with` statement can also be used to measure code time
> Named tracking points can be added with the `track` function

```python
import timy

with timy.Timer() as timer:
    N = 10000000
    for i in range(N):
        if i == N/2:
            timer.track('Half way')
            
>> Timy (Half way) 0.557577 seconds
>> Timy 0.988087 seconds            
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
            if n % i == 0:
                add_factor(i)
                n //= i
            else:
                i += 1
        return factors + [n]

factors = prime_factors(600851475143)
print(factors)

>> Factors (Found a factor) 0.000017 seconds
>> Factors (Found a factor) 0.000376 seconds
>> Factors (Found a factor) 0.001547 seconds
>> Factors 0.001754 seconds
>> [71, 839, 1471, 6857]
```

### Configuring

#### Importing timy config

```python
from timy.settings import timy_config
```

#### Enable or disable timy trackings
You can enable or disable timy trackings with the `tracking` value.
> The default value of `tracking` is `True`

```python
timy_config.tracking = False
```

#### Changing the way timy outputs information
You can choose between print or logging for all timy outputs by setting the
value of `tracking_mode`.
> The default value of `tracking_mode` is `TrackingMode.PRINTING`.

```python
from timy.settings import (
    timy_config,
    TrackingMode
)

timy_config.tracking_mode = TrackingMode.LOGGING
```

timy logs at the INFO level, which is not printed or stored by default. To
configure the logging system to print all INFO messages do
```
import logging
logging.basicConfig(level=logging.INFO)
```
or to configure the logging system to print only timy's INFO messages do
```
import logging
logging.basicConfig()
logging.getLogger('timy').level=logging.INFO
```

## Contribute
Contributions are **always** welcome, but keep it simple and small.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


## Changelog

### v 0.4.0 (September 23, 2017)

- Drops py2 support and adds 100% coverage with CI integration

### v 0.3.3 (April 19, 2017)

- Adds an optional argument `include_sleeptime` to count time elapsed including sleep time (`include_sleeptime=True`) and excluding sleep time (`include_sleeptime=False`)
