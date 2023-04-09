# system

You are helping a programmer write a Python function given only the expected inputs and outputs of that function. Your response should be exactly one Python function with the implementation of the function, and nothing else. Do not include any explanation in your reponse.

# user

`fql` is a function that inputs a number and outputs a number. The following are examples of the behavior of `fql`:

```
$f(0) = 0
f(2) = 4
f(4) = 16
f(6) = 36

```

Write a Python function `fql` that has this behavior.

# assistant

def fql(x):
    return x * x

