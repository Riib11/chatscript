from os import path
import json
from Conversation import *

convo = Conversation("conversations/pseudocoding")

convo.system("""
You are a programming assistant. You should help the user implement and analyze the behavior of programs.
""")

convo.user("""
The following is a pseudocode description of a function. Write a Python implementation of the function. Reply with only the Python implementation in a code block delimited by triple backticks, and nothing else.

fdx(x):
  convert x to string
  let n be length of x
  let m be the divisors of n
  convert m to string
  return length of m
""")

convo.assistant()

convo.save()
convo.write()

convo.user("""
What is result of `fdx(2 * 8)`?
""")

convo.assistant()
convo.save()
convo.write()

convo.user("""
You're close, but not quite right. Re-assess what the result of `str(m)` should be.
""")

convo.assistant()
convo.save()
convo.write()
