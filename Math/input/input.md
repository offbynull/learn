```{title}
Mathematics
```

```{toc}
```

# Place Value System

Modern number systems like the ones used today are called `{bm} place value system`s. The idea is that a number is represented as a string of symbols, where...

* each symbol represents a value
* each index represents a value

, and these symbol values and index values are combined using an algorithm to come up with the overall value of the string. For example, imagine a toy place value system that uses the following 4 symbols...

| Symbol | Value |
| ------ | ----- |
| A      |       |
| B      | □     |
| C      | □□    |
| D      | □□□   |

The value of the string DCADB is determined by first calculating the values of each index of the string. The value for each index is ...

```
_ _ _ _ _
| | | | |
| | | |  - □
| | |  --- □□
| |  ----- □□□
|  ------- □□□□
 --------- □□□□□

Note how the value increments as the position goes from right-to-left.
```

Then, for each position, add the value of that position repeatedly n times, where n is the value of the symbol at that position. Starting from right-to-left, ...

 * D - positional value is □□□□□ / symbol value = □□□.

   | Symbol Iteration | Positional Value | Symbol-position Value |
   | ---------------- | ---------------- | --------------------- |
   | □                | □□□□□            | □□□□□                 |
   | □                | □□□□□            | □□□□□ □□□□□           |
   | □                | □□□□□            | □□□□□ □□□□□ □□□□□     |

   Symbol-position value = □□□□□ □□□□□ □□□□□.

 * C - positional value is □□□□ / symbol value = □□.

   | Symbol Iteration | Positional Value | Symbol-Position Value |
   | ---------------- | ---------------- | --------------------- |
   | □                | □□□□             | □□□□                  |
   | □                | □□□□             | □□□□ □□□□             |

   Symbol-position value = □□□□ □□□□.

 * A - positional value is □□□ / symbol value = {none}.
   
   ```
   no-op
   ```

   Symbol-position value = {empty}.
 
 * D - positional value is □□ / symbol value = □□□.

   | Symbol Iteration | Positional Value | Symbol-Position Value |
   | ---------------- | ---------------- | --------------------- |
   | □                | □□               | □□                    |
   | □                | □□               | □□ □□                 |
   | □                | □□               | □□ □□ □□              |

   Symbol-position value = □□ □□ □□.

 * B - positional value = □ / symbol value = □.

   | Symbol Iteration | Positional Value | Symbol-Position Value |
   | ---------------- | ---------------- | --------------------- |
   | □                | □                | □                     |

   Symbol-position value = □.

The final value is for the string is calculated by combining (adding) all the symbol-position values together:

```
D C A D B
| | | | |
| | | |  - □
| | |  --- □□ □□ □□
| |  ----- 
|  ------- □□□□ □□□□
 --------- □□□□□ □□□□□ □□□□□

DCADB = □□□□□ □□□□□ □□□□□ □□□□ □□□□ □□ □□ □□ □
```

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

TODO CONTINUE FROM https://cnx.org/contents/yqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers

# Order of Operations

The `{bm} order of operations` are as follows:

1. Brackets
1. Exponents
1. Division and Multiplication (evaluated left-to-right)
1. Addition and Subtraction (evaluated left-to-right)

These rules are often abbreviated as either...

* `{bm} BEDMAS` - Brackets / Exponents / Division and Multiplication / Addition and Subtraction
* `{bm} PEMDAS` - Parenthesis / Exponents / Multiplication and Division / Addition and Subtraction

Note that these 2 are essentially the same. Division and multiplication are swapped, but since division and multiplication are evaluated left-to-right in the same step, it makes no difference.

# Algebra Rules

KEEP WORKING ON THESE:
ADD FRACTION ADDING AND MULTIPLICATION RULES (recipriocals, cross multiply, etc..)
ADD REMAINING ALGEBRA RULES
https://en.wikiversity.org/wiki/Algebraic_Properties_of_Equality
https://en.wikiversity.org/wiki/Basic_Laws_of_Algebra
http://www.themathpage.com/aPreCalc/algebraPre.htm (specifically 1, 6, and 7?)
ADD TRIVIAL AND NON-TRIVIAL EXAMPLES


Commutative Property

* `{kt} a \cdot b = b \cdot a`
* `{kt} a + b = b + a`

Associative Property

* `{kt} (a + b) + c = a + (b + c)`
* `{kt} (a \cdot b) \cdot c = a \cdot (b \cdot c)`

Distributive Property

* `{kt} a(b+c) = a \cdot b + a \cdot c`
* `{kt} a(b \cdot c) = a \cdot b \cdot a \cdot c`

Identity Property

* `{kt} a \cdot 1 = 1 \cdot a = a`
* `{kt} a + 0 = 0 + a = a`

Additive Inverse Property

* `{kt} a + (-a) = -a + a = 0`

Multiplicative Inverse / Multiplicative Reciprocal Property

* `{kt} a \cdot \frac{1}{a} = \frac{1}{a} \cdot a = 1`