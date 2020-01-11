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

TODO: DISCUSS DECIMAL PLACE AND FRACTIONAL PORTION. ACCURATELY DISCUSS DIGITS.

## Words

TODO: Discuss number to word transitions (2nd part of Chapter 1.1)

21,055 is the same as saying twenty one thousand fifty five

## Addition

TODO: Chapter 1.2

## Subtraction

## Multiplication

## Division

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

## Chapter 1 Section 1.1

__TRY IT__

1.1)

* a) 0 = {whole}
* b) 2/3 = {}
* c) 2 = {whole, counting}
* d) 9 = {whole, counting}
* e) 11.8 = {}
* f) 241 = {whole, counting}
* g) 376 = {whole, counting}

1.2)

* a) 0 = {whole}
* b) 5/3 = {}
* c) 7 = {whole, counting}
* d) 8.8 = {}
* e) 13 = {whole, counting}
* f) 201 = {whole, counting}

1.3) 176

1.4) 237

1.5) 63,407,218

* a. 7 -> ten millions place.
* b. 0 -> tens place.
* c. 1 -> hundred thousands place.
* d. 6 -> millions place.
* e. 3 -> ones place.

1.6) 27,493,615

* a) 2 -> billions place.
* b) 1 -> ten thousands place.
* c) 4 -> tens place.
* d) 7 -> hundred thousands place.
* e) 5 -> hundred millions place.

1.7) 9,258,137,904,061

```
9   -> nine trillion
258 -> two hundred fifty eight billion
137 -> one hundred thirty seven million
904 -> nine hundred and four thousand
061 -> sixty one
```

1.8) 17,864,325,619,004

```
17  -> seventeen trillion
864 -> eight hundred sixty four billion
325 -> three hundred twenty five million
619 -> six hundred nineteen thousand
004 -> and four
```

1.9) 316,128,839

```
316 -> three hundred sixteen million 
128 -> one hundred twenty eight thousand
839 -> eight hundred thirty nine
```

1.10) 31,536,000

```
31  -> thirty one
536 -> five hundred thirty six thousand
000 ->
```

1.11) fifty-three million, eight hundred nine thousand, fifty-one -> 536,809,051

1.12) two billion, twenty-two million, seven hundred fourteen thousand, four hundred sixty-six -> 2,022,714,466

1.13) 34 million -> 34,000,000

1.14) 204 million -> 204,000,000

1.15) 157 rounded to nearest ten: 160

1.16) 884 rounded to nearest ten: 880

1.17) 17,852 rounded to nearest hundred: 17,900

1.18) 4,951 rounded to nearest hundred: 5,000

1.19) 63,921 rounded to nearest thousand: 64,000

1.20) 156,437 rounded to nearest thousand: 156,000

__EXERCISE__

1.1.1)

* 0 = {whole}
* 2/3 = {}
* 5 = {counting, whole}
* 8.1 = {}
* 125 = {counting, whole}

1.1.2)

* 0 = {whole}
* 7/10 = {}
* 3 = {counting, whole}
* 20.5 = {}
* 300 = {counting, whole}

1.1.3)

* 0 = {whole}
* 4/9 = {}
* 3.9 = {}
* 50 = {counting, whole}
* 221 = {counting, whole}

1.1.4)

* 0 = {whole}
* 3/5 = {}
* 10 = {counting, whole}
* 303 = {counting, whole}
* 422.6 = {}

1.1.5) 561

1.1.6) 384

1.1.7) 461

1.1.8) 620

1.1.9) 579,601

* a) 9 -> thousands place
* b) 6 -> hundreds place
* c) 0 -> tens place
* d) 7 -> ten thousands place
* e) 5 -> hundred thousands place

1.1.10) 398,127

* a) 9 -> ten thousands place
* b) 3 -> hundred thousands place
* c) 2 -> tens place
* d) 8 -> thousands place
* e) 7 -> ones place

1.1.11) 56,804,379

* a) 8 -> hundred thousands place
* b) 6 -> millions place
* c) 4 -> thousands place
* d) 7 -> tens place
* e) 0 -> ten thousands place

1.1.12) 78,320,465

* a) 8 -> millions place
* b) 4 -> hundreds place
* c) 2 -> ten thousands place
* d) 6 -> tens place
* e) 7 -> ten millions place

1.1.13) 1,078 -> one thousand seventy eight

1.1.14) 5,902 -> five thousand nine hundred two

1.1.15) 364,510 -> three hundred sixty four thousand five hundred ten

1.1.16) 146,023 -> one hundred forty six thousand twenty three

1.1.17) 5,846,103 -> five million eight hundred forty six thousand one hundred three

1.1.18) 1,458,398 -> one million four hundred fifty eight thousand three hundred ninety eight

1.1.19) 37,889,005 -> thirty seven million, eight hundred eighty nine thousand five

1.1.20) 62,008,465 -> sixty two million eight thousand four hundred sixty five

1.1.21) 14,410 -> fourteen thousand four hundred ten

1.1.22) 12,276 -> twelve thousand two hundred seventy six

1.1.23) 613,000 -> six hundred thirteen thousand

1.1.24) 525,600 -> five hundred twenty five thousand six hundred

1.1.25) 2,617,176 -> two million six hundred seventeen thousand one hundred seventy six

1.1.26) 2,718,782 -> two million seven hundred eighteen thousand seven hundred eighty two

1.1.27) 23,867,000 -> twenty three million eight hundred sixty seven thousand

1.1.28) 20,665,415 -> twenty million six hundred sixty five thousand four hundred fifeteen

1.1.29) 1,377,583,156 -> one billion three hundred seventy seven million five hundred eighty three thousand one hundred fifty six

1.1.30) 1,267,401,849 -> one billion two hundred sixty seven million four hundred one thousand eight hundred forty nine

1.1.31) four hundred twelve -> 412

1.1.32) two hundred fifty-three -> 253

1.1.33) thirty-five thousand, nine hundred seventy-five -> 35,975

1.1.34) sixty-one thousand, four hundred fifteen -> 61,415

1.1.35) eleven million, forty-four thousand, one hundred sixty-seven -> 11,044,167

1.1.36) eighteen million, one hundred two thousand, seven hundred eighty-three -> 18,102,783

1.1.37) three billion, two hundred twenty-six million, five hundred twelve thousand, seventeen -> 3,226,512,17

1.1.38) eleven billion, four hundred seventy-one million, thirty-six thousand, one hundred six -> 11,471,036,106

1.1.39) seven billion, one hundred seventy-three million -> 7,173,000,000

1.1.40) four billion, five hundred sixty-eight million years -> 4,568,000,000

1.1.41) thirty-nine trillion -> 39,000,000,000

1.1.42) three trillion, five hundred billion -> 3,500,000,000

1.1.43) round to nearest ten 

* a) 386 -> 390
* b) 2,931 -> 2,930

1.1.44) round to nearest ten 

* a) 792 -> 790
* b) 5,647 -> 5,650

1.1.45) round to nearest hundred

* a) 13,748 -> 13,700
* b) 391,794 -> 391,800

1.1.46) round to nearest hundred

* a) 28,166 -> 28,200
* b) 481,628 -> 481,600

1.1.47) round to nearest ten

* a) 1,492 -> 1,490
* b) 1,497 -> 1,500

1.1.48) round to nearest thousand

* a) 2,391 -> 2,000
* b) 2,795 -> 3,000

1.1.49) round to nearest hundred

* a) 63,994 -> 64,000
* b) 63,949 -> 63,900

1.1.50) round to nearest thousand

* a) 163,584 -> 164,000
* b) 163,246 -> 163,000

1.1.51) 24,493 -> twenty four thousand four hundred ninety three

1.1.52) 18,549 -> eighteen thousand five hundred forty nine

1.1.53) round 24,493 to the nearest...

* a) ten -> 24,490
* b) hundred -> 24,500
* c) thousand -> 24,000
* d) ten thousand -> 20,000

1.1.54) round 18,549 to the nearest...

* a) ten -> 18,550
* b) hundred -> 18,500
* c) thousand -> 19,000
* d) ten-thousand 20,000

1.1.55) round 1,355,692,544 to the nearest...

* a) billion -> 1,000,000,000
* b) hundred-million -> 1,400,000,000
* c) million -> 1,356,000,000

1.1.56) round 149,597,888 to the nearest...

* a) hundred-million -> 100,000,000
* b) ten-million -> 150,000,000
* c) million -> 150,000,000

1.1.57)

The difference between counting numbers and whole numbers is that counting numbers start at 1 while whole numbers start at 0. The reason is that counting numbers are used when you're counting something. You usually need to have 1 of something to start counting. For example, I can't count the number of apples if there are no apples. I need at least 1 apple to be able to count.

1.1.58)

It's easier to say numbers that are rounded. For example...

58,123 -> fifty eight thousand one hundred twenty three
58,000 -> fifty eight thousand

Less words to speak while conveying approximately the same quantity.

## Chapter 1 Section 1.2

__TRY IT__

1.21) write out...

* a) 8+4 -> eight plus four
* b) 18+11 -> eighteen plus eleven

1.22) write out...

* a) 8+4 -> eight plus four
* b) 18+11 -> eighteen plus eleven

1.23) model 3 + 6...

```
□□□ □□□□□□
 3    6
```

1.24) model 5 + 1...

```
□□□□□ □
  5   1
```

1.25) model 5 + 7...

```
□□□□□ □□□□□□□
  5      7
```

1.26) model 6 + 8...

```
□□□□□□ □□□□□□□□
   6       8
```

1.27) model 15 + 27...

```
□□□□□□□□□□   □□□□□□□□□□
  □□□□□      □□□□□□□□□□
              □□□□□□□
    15          27
```

1.28) model 16 + 29...

```
□□□□□□□□□□   □□□□□□□□□□
  □□□□□□     □□□□□□□□□□
             □□□□□□□□□
    16           29
```

1.29)

a) 0+19=19
b) 39+0=39

1.30)

a) 0+24=24
b) 57+0=57

1.31) 9+7=16 and 7+9=16

1.32) 8+6=14 and 6+8=14

1.33) 32+54

```
32
54 +
--
86
```

1.34) 25+74

```
25
74 +
--
89
```

1.35) 35+98

```
 1  <-- carry over
 35
 98 +
 --
133
```

1.37) 456+376

```
 11  <-- carry over
 456
 376 +
 --- 
1032
```

1.38) 269+578

```
 11  <-- carry over
 269
 578 +
 --- 
 847
```

1.39) 4597+685

```
 111  <-- carry over
 4597
  685 +
 ----
 5282
```

1.40) 5837+695

```
 111  <-- carry over
 5837
  695 +
 ----
 5282
```

1.41) 46195+397+6281

```
 1 21  <-- carry over
 46195
   397
  6281 +
 -----
 52873
```

1.42) 53762+196+7458

```
 1121  <-- carry over
 53762
   196
  7458 +
 -----
 61416
```

1.43) 17+26=43

1.44) 28+14=42

1.45) 29+76=105

1.46) 37+69=106

1.47) 18+15+26+49+32=140

1.48) 230+165+325=720

1.49) 3+3+3+2+2+4+4+9=32

1.50) 4+4+2+2+4+6+12+2=36


CONTINUE FROM EXERCISE PROBLEM 1

CONTINUE FROM EXERCISE PROBLEM 1

CONTINUE FROM EXERCISE PROBLEM 1

CONTINUE FROM EXERCISE PROBLEM 1

CONTINUE FROM EXERCISE PROBLEM 1

CONTINUE FROM EXERCISE PROBLEM 1