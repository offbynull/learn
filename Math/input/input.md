```{title}
Mathematics
```

```{toc}
```

# Place Value System

Modern number systems like the ones used today are called `{bm} place value system`s. The idea is that a number is represented as a string of symbols, where...

* each symbol represents a value.
* each index represents a value.

These symbol values and index values are combined using an algorithm to come up with the overall value of the string:

```
for (symbol_value, index_value) in input
    for item in symbol_value
        final_value = concat(final_value, index_value)
```

For example, imagine a toy place value system that uses the following 4 symbols: ABCD. To calculate the value for string `DCADB`, begin by first determining the value for each symbol (`symbol_value`)...

| Symbol | Value |
| ------ | ----- |
| A      |       |
| B      | □     |
| C      | □□    |
| D      | □□□   |

```{note}
The value increments for each symbol.
```

Then, calculate the value for each index (`index_value`) ...

```
_ _ _ _ _
| | | | |
| | | |  - □
| | |  --- □□
| |  ----- □□□
|  ------- □□□□
 --------- □□□□□
```

```{note}
The value increments as the index goes from right-to-left.
```

Now that the `symbol_value`s and `index_value`s are known, the algorithm can be run on the string. For each `(symbol_value, index_value)` in the string `DCADB`...

 * `D _ _ _ _` (`symbol_value = □□□` / `index_value = □□□□□`)

   ```
   for item in symbol_value
       final_value = concat(final_value, index_value)
   ```

   | symbol_value | index_value | item | final_value       |
   | ------------ | ----------- | ---- | ----------------- |
   | □□□          | □□□□□       | □    | □□□□□             |
   | □□□          | □□□□□       | □    | □□□□□ □□□□□       |
   | □□□          | □□□□□       | □    | □□□□□ □□□□□ □□□□□ |

 * `_ C _ _ _` (`symbol_value = □□` / `index_value = □□□□`)
   
   ```
   for item in symbol_value
       final_value = concat(final_value, index_value)
   ```

   | symbol_value | index_value | item | final_value       |
   | ------------ | ----------- | ---- | ----------------- |
   | □□           | □□□□        | □    | □□□□              |
   | □□           | □□□□        | □    | □□□□ □□□□         |

 * `_ _ A _ _` (`symbol_value = ` / `index_value = □□□`)
   
   ```
   for item in symbol_value
       final_value = concat(final_value, index_value)
   ```
   
   ```
   no-op
   ```

   Symbol-position value = {empty}.
 
 * `_ _ _ D _` (`symbol value = □□□` / `index_value = □□`)

   ```
   for item in symbol_value
       final_value = concat(final_value, index_value)
   ```

   | symbol_value | index_value | item | final_value       |
   | ------------ | ----------- | ---- | ----------------- |
   | □□□          | □□          | □    | □□                |
   | □□□          | □□          | □    | □□ □□             |
   | □□□          | □□          | □    | □□ □□ □□          |

 * `_ _ _ _ B` (`symbol value = □` / `index_value = □`)

   ```
   for item in symbol_value
       final_value = concat(final_value, index_value)
   ```

   | symbol_value | index_value | item | final_value       |
   | ------------ | ----------- | ---- | ----------------- |
   | □            | □           | □    | □                 |

The value for the string is...

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

# OpenStax Prealgebra Problems

## Chapter 1

__TRY IT 1.1__

* `{kt} 0` = {whole}
* `{kt} \frac{2}{3}` = {}
* `{kt} 2` = {whole, counting}
* `{kt} 9` = {whole, counting}
* `{kt} 11.8` = {}
* `{kt} 241` = {whole, counting}
* `{kt} 376` = {whole, counting}

__TRY IT 1.2__

* `{kt} 0` = {whole}
* `{kt} \frac{5}{3}` = {}
* `{kt} 7` = {whole, counting}
* `{kt} 8.8` = {}
* `{kt} 13` = {whole, counting}
* `{kt} 201` = {whole, counting}

__TRY IT 1.3__

176

__TRY IT 1.4__

237

__TRY IT 1.5__

 * a. ten millions place.
 * b. tens place.
 * c. hundred thousands place.
 * d. millions place.
 * e. ones place.

__TRY IT 1.6__

 * a. billions place.
 * b. ten thousands place.
 * c. tens place.
 * d. hundred thousands place.
 * e. hundred millions place.

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)

https://cnx.org/contents/ayqV9q0HH@20.1:gUzCHLwU@17/1-1-Introduction-to-Whole-Numbers (CONTINUE FROM Use Place Value to Name Whole Numbers)