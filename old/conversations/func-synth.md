# system

You are helping a programmer write a Python function given only the expected inputs and outputs of that function. Your response should be exactly one Python function with the implementation of the function, and nothing else. Do not include any explanation in your reponse.

The function should only use integer addition, subtraction, and multiplication. It should not use any other operations.

# user

`foo` is a function that inputs a number and outputs a number. The following are examples of the expected inputs and outputs of `foo`:

```
foo(0) = 2
foo(1) = 4
foo(2) = 6
foo(3) = 8
foo(4) = 10
foo(5) = 12
foo(6) = 14
foo(7) = 16
foo(8) = 18
foo(9) = 20

```

Write a Python function `foo` that has this behavior.

# assistant

def foo(n):
    return 2 * n + 2

