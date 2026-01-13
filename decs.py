#decorators
from functools import wraps
import time

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

@timed
def compute_sum(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total

print(compute_sum(1_000_000_00))