# InterLLM

Interfaces for LLMs.

I want to teach an LLM how to use designed tools i.e. programs.

The general framework for giving something tools use is an _interface_, which defines all of the different actions that the tool can do.

## Methodology

I expect that the LLM knows enough about programming that I can describe an interface in a program-like way. So, an interface can be defined as a collection of:
- _types_: atomic things that can be manipulated via functions but the contents of which cannot be inspected
- _functions_: accepts some inputs and yields some outputs

## Examples

Teaching the LLM to use a calculator.

**System message.**
> You are a arithmetic assistant. The user will ask complicated mathematical questions. In order to answer the questions, 