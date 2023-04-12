# system

You are a programming assistant. You should help the user implement and analyze the behavior of programs.

# user

The following is a pseudocode description of a function. Write a Python implementation of the function. Reply with only the Python implementation in a code block delimited by triple backticks, and nothing else.

input x
convert x to string
let n be length of x
return divisors of n

# assistant

```
def divisors_of_x_length(x):
    x_str = str(x)
    n = len(x_str)
    divisors = [i for i in range(1, n+1) if n % i == 0]
    return divisors
```

# user

What is the result of `divisors_of_x_length(148)`?

# assistant

The result of `divisors_of_x_length(148)` is `[1, 2, 3]`.

