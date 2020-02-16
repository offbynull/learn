```{title}
Mathematics
```

```{toc}
```

# Place Value System

The `{bm} place value system/(place value system|place-value system|place value notation|place-value notation|positional numeral system)/i` is the modern way in which numbers are represented. A number represented using the place value system is made up of a string of symbols separated by a dot, where each (index, symbol) combination in the string represents a value (i.e. `val[idx] = compute(idx, str[idx])`).


The symbols used to represent a number are called `{bm} digit`s. All digits to the...

 * left of the dot represents wholes.
 * right of the dot represents a partial (less than a whole).

These wholes and partial are combined to represent the final value for the number. The exact grammar and algorithm for computing the final value is detailed below.

```
●●●●●●●●●●
●●●●●●●●●●
●●●●●●●●●●
●●●●●●●●●●  ●●●     ◑
    4        3   .  5
```

The grammar for the place value system is...

```antlr
number: whole (DOT partial)?;
whole: DIGIT+;
partial: DIGIT+;

DOT: '.';
DIGIT: [0123456789];
```

The entry point to the grammar is the number rule. Note that the partial portion of the number rule is optional -- a number with a missing partial portion is assumed to have a partial portion of 0 (e.g. 5 is the same as 5.0).

The details below describe each sub-rule as well as the algorithm to process that sub-rule. None of the algorithms use actual numbers / number operations -- value is tracked by iteratively pushing blocks into arrays.

```{note}
Why create an algorithm without using numbers? Using numbers to describe numbers is circular logic.
```

**whole rule**

```
number: whole ('.' partial)?;
         │
         └── DIGIT+;
```

The whole rule is used to express how many whole values there are. For example, to process the string 572 for the whole rule, ...

 1. begin by first determining the value each digit represents...

    ```
    0 = <empty>
    1 = ●
    2 = ●●
    3 = ●●●
    4 = ●●●●
    5 = ●●●●●
    6 = ●●●●●●
    7 = ●●●●●●●
    8 = ●●●●●●●●
    9 = ●●●●●●●●●
    ```


 2. Then, calculate the value for each index of the string 572. The algorithm for determining the value of each index is...

    ```
    index_values = []
    for (item in index) {
      next_index_value = <empty>
      if (index_values.isEmpty()) {
        index_values.push(●)
      } else {
        last_index_value = index_value[-1]
        for (inner_item in ●●●●●●●●●●) {   // the number of dots here should be 1 more than the value of the largest symbol
          next_index_value.push(last_index_value)
        }
      }
    }
    index_values.reverse()
    ```

    ..., so for the string 572, the index values would be...

    ```
    _ _ _
    │ │ │
    │ │ └─ ● 
    │ └─── ●●●●●●●●●●
    └───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    ```

 3. Now that the digit values and index values are known, the value of each (digit, index) combination can be calculated. The algorithm for determining the value of each (digit, index) combination is...

    ```
    final_value = <empty>
    for (digit_value, index_value) in input
      value = <empty>
      for item in digit_value
        value.push(index_value)
    ```

    ... , so each (digit, index) in the number 572 would be computed as...

    * 5\_\_

      ```
      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
      ```

    * \_7\_
      
      ```
      ●●●●●●●●●●
      ●●●●●●●●●●
      ●●●●●●●●●●
      ●●●●●●●●●●
      ●●●●●●●●●●
      ●●●●●●●●●●
      ●●●●●●●●●●
      ```

    * \_\_2
      
      ```
      ●
      ●
      ```

    Those values combined together would be...

    ```
    5 7 2
    │ │ │
    │ │ └─ ●
    │ │    ● 
    │ │
    │ └─── ●●●●●●●●●●
    │      ●●●●●●●●●●
    │      ●●●●●●●●●●
    │      ●●●●●●●●●●
    │      ●●●●●●●●●●
    │      ●●●●●●●●●●
    │      ●●●●●●●●●●
    │
    └───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    ```

**partial rule**

```
number: whole ('.' partial)?;
                      │
                      └── DIGIT+;
```

```{note}
It's expected that you fully understand the whole rule because whole numbers are used to explain the partial rule.
```

```{define-block}
diagramhelperpartrecurse
diagramhelperpartrecurse_macro/
diagramhelper_code/target/appassembler/
```

The partial rule is used to express a portion of a whole. In other words, some value that is less than a whole.

If the partial rule is not set, it's assumed to be 0.

Conceptually, you can think of each digit in the partial string as a recursive slicing of a single whole. For example, in the partial string 358, the first index picks out 3 equal parts out of the whole ...

```{diagramhelperpartrecurse}
3
```

, ... the second index picks out 5 equal parts out of the NEXT part of the whole ...

```{diagramhelperpartrecurse}
35
```

, ... the third index picks out 8 equal parts out of the NEXT part of the previous part ...

```{diagramhelperpartrecurse}
358
```

.

```{note}
Trouble seeing this final partition? Open the above image up standalone and zoom in. It's an SVG.
```

This is exactly the same as chopping up a whole into 1000 equal parts and picking 358 of those parts...

```{define-block}
diagramhelperpart
diagramhelperpart_macro/
diagramhelper_code/target/appassembler/
```

```{diagramhelperpart}
358
```

The algorithm for processing the partial rule is similar to the conceptual model. For example, to process the string 55 for the partial rule, ...

 1. begin by determining the total number of parts there are. The algorithm to do this is as follows..

    ```
    total_parts = <empty>
    for (item in index) {
      if (total_parts == <empty>) {
        total_parts.push(●●●●●●●●●●) // the number of dots here should be 1 more than the value of the largest digit
      } else {
        new_total_parts = <empty>
        for (inner_item in ●●●●●●●●●●) {  // the number of dots here should be 1 more than the value of the largest digit
          new_total_parts.push(total_parts)
        }
        total_parts = new_total_parts
      }
    }
    ```

    ..., so for the string 55, the total number of parts would be 100...

    ```
    ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    ```

    ```{note}
    An easier way to do the same thing is...
     1. add an extra index.
     1. set the first index to 1.
     1. set all other indexes to 0.
     
    So if the partial string has 2 digits (as 55 does), the total number of parts would be 100.

    The reason why the code above doesn't do this is because I'm trying to avoid the use of numbers and operations that haven't been introduced yet.
    ```

    ```{note}
    An easier way to do the same thing is 10^partial.length.
     
    So if the partial string has 2 digits (as 55 does), the total number of parts would be 10^2=100.

    The reason why the code above doesn't do this is because I'm trying to avoid the use of numbers and operations that haven't been introduced yet.
    ````

 2. The partial string is a selection out the total parts calculated in the step above. Out of 100 parts, 55 are selected.

    ```
    [●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●]●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    ```

    ```{diagramhelperpart}
    55
    ```

# Number Naming

TODO: Discuss number to word transitions (2nd part of Chapter 1.1)

21,055 is the same as saying twenty one thousand fifty five

# Real Numbers

```{plantuml}
@startditaa(--no-separation)
+-----------------------------------------------------------------------+
|                                                                       |
|                                 Real cFFF                             |
|                                                                       |
|   +-+-+-+----------------------------+   +------------------------+   |
|   | | | |                            |   |                        |   |
|   | | | |   Natural (e.g. 1, 7, 291) |   |                        |   |
|   | | | |   cFFF                     |   |                        |   |
|   | | | +----------------------------+   |                        |   |
|   | | |                              |   |                        |   |
|   | | |   Whole (0)                  |   |                        |   |
|   | | |   cFFF                       |   |                        |   |
|   | | +------------------------------+   | Irrational (π, √2, √3) |   |
|   | |                                |   | cFFF                   |   |
|   | |   Integer (-7, -19, -471)      |   |                        |   |
|   | |   cFFF                         |   |                        |   |
|   | +--------------------------------+   |                        |   |
|   |                                  |   |                        |   |
|   |   Rational (⅓, -⅓, -⅑)           |   |                        |   |
|   |   cFFF                           |   |                        |   |
|   +----------------------------------+   +------------------------+   |
+-----------------------------------------------------------------------+
@endditaa
```

TODO: write blurb here

## Natural

TODO: write blurb here

## Whole

```{plantuml}
@startditaa(--no-separation)
+-----------------------------------------------------------------------+
|                                                                       |
|                                 Real cFFF                             |
|                                                                       |
|   +-+-+-+----------------------------+   +------------------------+   |
|   | | | |                            |   |                        |   |
|   | | | |   Natural (e.g. 1, 7, 291) |   |                        |   |
|   | | | |   cCCF                     |   |                        |   |
|   | | | +----------------------------+   |                        |   |
|   | | |                              |   |                        |   |
|   | | |   Whole (0)                  |   |                        |   |
|   | | |   c88F                       |   |                        |   |
|   | | +------------------------------+   | Irrational (π, √2, √3) |   |
|   | |                                |   | cFFF                   |   |
|   | |   Integer (-7, -19, -471)      |   |                        |   |
|   | |   cFFF                         |   |                        |   |
|   | +--------------------------------+   |                        |   |
|   |                                  |   |                        |   |
|   |   Rational (⅓, -⅓, -⅑)           |   |                        |   |
|   |   cFFF                           |   |                        |   |
|   +----------------------------------+   +------------------------+   |
+-----------------------------------------------------------------------+
@endditaa
```

`{bm} Whole number`s are numbers which have no partial (fractional) portion -- they only consist of wholes. For example, 5, 104, and 27 are whole numbers while 4.2 is not. Whole numbers include all of the `{bm} natural number/(natural number|counting number)/i`s as well as 0.

## Integer

TODO: this was pulled out from the place-value system section -- fix it.

```
number: sign? whole ('.' partial)?;
         │
         └── sign: POSITIVE | NEGATIVE;
```

The sign rule is used to express which category a number is in. Recall that the number 0 represents nothing / no value / empty values. If the sign is ...

* NEGATIVE, it means that it's less than nothing.
* POSITIVE, it means that it's more than nothing.

If the sign is not set, it's assumed to be POSITIVE.

Conceptually, you can think of the sign rule as putting numbers onto different sides of a line, where 0 is the dividing point. The numbers on the negative side of the line are the opposites to the positive side of the line (and vice versa).

```{define-block}
diagramhelperlinenum
diagramhelperlinenum_macro/
diagramhelper_code/target/appassembler/
```

```{diagramhelperlinenum}
width 600
- -3.5
| -3
| -2.5
| -2
| -1.5
| -1
| -0.5
| 0
| 0.5
| 1
| 1.5
| 2
| 2.5
| 3
- 3.5
```

For example, if I used the number 5 to represent how many steps I moved up, the number -5 would represent how many steps I moved down. This is because down is the opposite of up (and vice versa).

```{diagramhelperlinenum}
width 600
- -5.5
* -5
| -4
| -3
| -2
| -1
| 0
| 1
| 2
| 3
| 4
* 5
- 5.5
```

In certain cases negative numbers represent a loss in value. For example, if monetary value were represented using a...
 * negative number, it means that money is lost / owed.
 * positive number, it means that money is gained / in possession.

```{note}
Remember that 0 means no value / nothing / empty. As such, there's no such thing as -0 or +0. There is just 0, and its used as a dividing point between the negatives and positives. If 0 has a sign, you can remove it.
```

There is no special algorithm for processing the sign rule -- set a flag to indicate if the number is negative or positive.

## Rational

TODO: Chapter 4

`{bm} Fraction`s are a way of representing numbers as parts. The syntax for a fraction is as follows...

`{kt} \frac{numerator}{denominator}`

... where the...
 * `{bm}numerator` (top) is an integer that represents the total number of parts.
 * `{bm}denominator` (bottom) is an integer that represents the number of parts in a whole.

For example, 4 parts out of 5 parts would be represented as `{kt} \frac{4}{5}`...

```{define-block}
diagramhelperfrac
diagramhelperfrac_macro/
diagramhelper_code/target/appassembler/
```

```{diagramhelperfrac}
radius 40
4
5
```

In some cases, the numerator may be greater than the denominator. That is, the total number of parts may be larger than the number of parts in a whole. For example, `{kt} \frac{11}{8}`...

```{diagramhelperfrac}
radius 40
11
8
```

In cases such as the example above, the wholes may be written as a single number and the partial portion may be expressed as a fraction: `{kt} 1 \frac{3}{8}`.

## Irrational

# Whole Number Addition

`{bm} Addition` is the concept of taking 2 numbers and combining their values together. For example, combining 3 items and 5 items together results in 7 items...

```
 [●●●]    [●●●●●]
   3         5

group values together

   [●●●●●●●●]
       7
```

Addition is typically represented using the infix operator +. The above example would be represented as 3+5.

```{note}
You can think of this as a function that takes in 2 arguments: add(3, 5).
```

When using words, addition is typically represented using the following syntax:

* `{bm} add` -- e.g. add 3 and 5
* `{bm} plus` -- e.g. 3 plus 5
* `{bm} sum` -- e.g. sum of 3 and 5
* `{bm} increase` -- e.g. 3 increased by 5
* `{bm} more than` -- e.g. 3 more than 5
* `{bm} total` -- e.g. total of 3 and 5

Properties of addition:

 * Order in which 2 numbers are added doesn't matter (commutative).
   
   ```
    [●●●]    [●●●●●] results in [●●●●●●●●]    (3+5 is 7)
      3         5                    7
   
    [●●●●●]   [●●●]  results in [●●●●●●●●]    (5+3 is 7)
      5         3                    7
   ```

 * Any number plus 0 results in the same number (identity).

   ```
   [●●●]    [] results in [●●●]    (3+0 is 3)
     3       0              3

   []    [●●●] results in [●●●]    (0+3 is 3)
    0      3                3
   ```

The algorithm used by humans to add large numbers together is called `{bm} vertical addition`. Vertical addition relies on two ideas...

1. humans can easily add a single digit number to another single digit number without much effort. For example...

   * 3+4 is 7
   * 1+9 is 10
   * 9+9 is 18

   ... are all addition operations that don't take much effort / are already probably cached in person's memory.

2. The second idea is that numbers represented in place-value notation can be broken down into single digit components -- the place of each digit in the number represents some portion of that number's value. For example, the number 935 can be broken down as 9 100s, 3 10s, and 5 1s...

   ```
   100
   100
   100
   100
   100            1
   100            1
   100     10     1
   100     10     1
   100     10     1
   ---     --     -
   900     30     5
   
   
   
   9 3 5
   │ │ │
   │ │ └─ ●
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │
   │ └─── ●●●●●●●●●●
   │      ●●●●●●●●●●
   │      ●●●●●●●●●●
   │
   └───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
   ```

Since a number can be broken down into single digit components and adding a single digit to any number is easy, any two numbers can be added by adding their individual single digit components. For example, the number 53 and 21 are broken down as follows...

```
5 3                      2 1
│ │                      │ │
│ └─ ●                   │ └─ ●
│    ●                   │
│    ●                   └─── ●●●●●●●●●●
│                             ●●●●●●●●●●
└─── ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

Add their individual single digit components together to get the sum. The ...
 * 1s place combines the 3 items and 1 item together to get 4 items: 3 + 1 results in 4
 * 10s place combines the 5 rows and 2 rows together to get 7 rows: 50 + 20 result in 70

```
7 4
│ │
│ └─ ●
│    ● 
│    ● 
│    ● 
│
└─── ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

In certain cases, the addition of two single digit components may bleed over to the next single digit component. For example, adding 93 and 21 can be broken down as follows...
 * 1s place combines the 3 items and 1 item together to get 4 items: 3 + 1 results in 4
 * 10s place combines the 9 rows and 2 rows together to get 7 rows: 90 + 20 result in 110

Combining the 10s place resulted in a bleed over to the hundreds place. This extra 100s place bleed over digit can be carried over and combined into the hundreds place. This process is called carry-over -- you're carrying-over the extra bleed over digit to its correct place and combining it with whatever else is there.

Conceptually, carrying-over is the idea of breaking out a group of 10 from the current place and moving them over to the next highest place (e.g. 10s place to 100s place). For example, when adding 93 to 21, adding the digits at the 10's place (90+20) results in 110...

```
9 3                      2 1
│ │                      │ │
│ └─ ●                   │ └─ ●
│    ●                   │
│    ●                   └─── ●●●●●●●●●●
│                             ●●●●●●●●●●
└─── ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●

results in 

11 4
│  │
│  └─ ●
│     ● 
│     ● 
│     ● 
│
└─── ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

Since 11 is too many digits for the tens place (each place must only have 1 digit), break out 10 groups from the 10s place and move those over to the 100s place...

```
11 4
│  │
│  └─ ●
│     ● 
│     ● 
│     ● 
│
└─── ●●●●●●●●●●
    ┌──────────┐
    │●●●●●●●●●●│
    │●●●●●●●●●●│ each group is 10 items and we grabbed 10 of them (that's 100 items total)
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    └──────────┘

move those 100 items as 1 group of 100s

1 1 4
│ │ │
│ │ └─ ●
│ │    ● 
│ │    ● 
│ │    ● 
│ │
│ └─── ●●●●●●●●●●
│     ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─────│●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●│
      └────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The digit in the 10s place is the result for the 10s place, while the digit in the 100s place gets combined in with the 100s place. In the above example, the 100s place was empty, so the carry-over remained as-is.

The way to perform this algorithm in real-life is to stack the two numbers being added on top of each other, where the positions for both numbers match up (e.g. the 1s position matches up, the 10s position matches up, the 100s position matched up, etc..). Then, add the individual single digit components together (from right-to-left). For example...

```{define-block}
ktvertadd
ktvertadd_macro/
kthelper_code/target/appassembler/
```

```{ktvertadd}
{1}{5}{3}
{ }{2}{1}
---
{1}{7}{4}
```

```{note}
The number 21 has nothing in its 100s place -- nothing is the same as 0. 21 is the same as 021.
```

If 2 individual single digit components combine together to results in an extra digit (e.g. 5+8=13), the bleed over digit is carried over to the next position (on the left). This is denoted by stacking the bleed over digit on top of the next position -- it's being combined along with the other digits at that position. For example...

```{ktvertadd}
{1}{ }{ }
{5}{5}{1}
{ }{8}{1}
---
{6}{3}{2}
```

The way to perform this algorithm via code is as follows...

```{output}
wholenum_code/src/main/java/com/offbynull/wholenum/MainAddition.java
java
//MARKDOWN_ISOLATE\s*\n([\s\S]+)\n\s*//MARKDOWN_ISOLATE
```

```{define-block}
wholenumadd
wholenumadd_macro/
wholenum_code/target/appassembler/
```

```{wholenumadd}
273 991
```

# Whole Number Subtraction

`{bm} Subtraction` is the concept of removing the value of one number from another number. For example, removing 3 items from 5 items results in 2 items...

```
    [●●●●●]
       5

pick out 3 from the 5

   [●●] [●●●]
    2     3
```

Subtraction is typically represented using the infix operator -. The above example would be represented as 5-3.

```{note}
You can think of this as a function that takes in 2 arguments: subtract(5, 3).
```

When using words, subtraction is typically represented using the following syntax:

* `{bm} minus` -- e.g. 5 minus 3
* `{bm} difference of` -- e.g. difference of 5 and 3
* `{bm} subtracted by` -- e.g. 5 subtracted by 3
* `{bm} decreased by` -- e.g. 5 decreased by 3
* `{bm} less than` -- e.g. 5 less than 3
* `{bm} subtracted from` -- e.g. 3 subtracted from 5

Properties of subtraction:

 * Any number subtracted by 0 results in the same number (identity).

   ```
   [●●●]    [] results in [●●●]    (3+0 is 3)
     3       0              3
   ```

```{note}
Unlike addition, subtraction is not commutative. 5-3 isn't the same as 3-5
```

The algorithm used by humans to subtract large numbers from each other is called `{bm} vertical subtraction`. Vertical subtraction relies on two ideas...

1. humans can easily subtract a small 1 to 2 digit numbers (anything smaller than 20) from each other without much effort. For example...

   * 4-3 is 1
   * 10-1 is 9
   * 15-3 is 13

   ... are all subtraction operations that don't take much effort / are already probably cached in person's memory.

2. The second idea is that numbers represented in place-value notation can be broken down into single digit components -- the place of each digit in the number represents some portion of that number's value. For example, the number 935 can be broken down as 9 100s, 3 10s, and 5 1s...

   ```
   100
   100
   100
   100
   100            1
   100            1
   100     10     1
   100     10     1
   100     10     1
   ---     --     -
   900     30     5
   
   
   
   9 3 5
   │ │ │
   │ │ └─ ●
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │
   │ └─── ●●●●●●●●●●
   │      ●●●●●●●●●●
   │      ●●●●●●●●●●
   │
   └───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
   ```

Since a number can be broken down into single digit components and subtracting a single digit to any number is easy, any two numbers can be subtracted by subtracting their individual single digit components. For example, the number 53 and 21 are broken down as follows...

```
5 3                      2 1
│ │                      │ │
│ └─ ●                   │ └─ ●
│    ●                   │
│    ●                   └─── ●●●●●●●●●●
│                             ●●●●●●●●●●
└─── ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

Subtract their individual single digit components from each other to get the difference. The ...
 * 1s place removes 1 item from 3 items to get 2 items: 3 - 1 results in 2
 * 10s place removes 2 rows from 5 rows together to get 3 rows: 50 - 20 result in 30

```
3 2
│ │
│ └─ ●
│    ● 
│
└─── ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

In certain cases, the subtraction of two single digit components may not be possible. For example, subtracting 91 and 23...

```
9 1                      2 3
│ │                      │ │
│ └─ ●                   │ └─ ●
│                        │    ●
└─── ●●●●●●●●●●          │    ●
     ●●●●●●●●●●          │
     ●●●●●●●●●●          └─── ●●●●●●●●●●
     ●●●●●●●●●●               ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

The ...
 * 1s place removes 3 items from 1 item to get ??? items: 1-3 is not possible 
 * 10s place removes the 2 rows from 9 rows to get 7 rows: 90 - 20 result in 70

The algorithm fails at the 1s place. It's impossible to remove 3 items from 1 item -- the most that can be removed from 1 item is 1 item. The way to handle this is to pick out 1 group from the 10s place and mover it over back to 1s place...

```
9 1                      2 3
│ │                      │ │
│ └─ ●                   │ └─ ●
│                        │    ●
└─── ●●●●●●●●●●          │    ●
     ●●●●●●●●●●          │
     ●●●●●●●●●●          └─── ●●●●●●●●●●
     ●●●●●●●●●●               ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
    ┌──────────┐
    │●●●●●●●●●●│ each group is 10 items and we grabbed 1 of them (that's 10 items total)
    └──────────┘

move those items back to the 1s place

8 11                     2 3
│ │                      │ │
│ └─ ●                   │ └─ ●
|   ┌─┐                  │    ●
│   │●│                  │    ●
│   │●│                  │
│   │●│                  └─── ●●●●●●●●●●
│   │●│                       ●●●●●●●●●●
│   │●│                  
│   │●│
│   │●│
│   │●│
│   │●│
│   │●│
│   └─┘
│
└─── ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

Now it's possible to subtract. The ...
 * 1s place removes 3 items from 11 item to get 8 items: 11-3 results in 8 
 * 10s place removes the 2 rows from 8 rows to get 6 rows: 80 - 20 result in 60

This process is called borrowing -- you're borrowing 1 group from the next largest position and moving those items back so that there's enough for subtraction to take place. In total, the value is still the same -- the total number of items (dots) doesn't change, but the items are being moved around so that the subtraction of a component can happen. 

In certain cases, a group may need to be borrowed but the next largest position is 0. For example, subtracting 100 and 11...

```
1 0 0                      1 1
│ │ │                      │ │
│ │ └─ ●                   │ └─ ●
│ │                        │
│ └─── <empty>             └─── ●●●●●●●●●●
│
└───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
```

Borrow recursively to handle this case:

* subtract 1s position: 0-1 not possible, borrow from 10s position

  * borrow from 10s position: can't borrow 10s position is 0, borrow from 100s position

    * borrow from 100s position: 100s position changes from 1 to 0

      ```
      1 0 0                      1 1
      │ │ │                      │ │
      │ │ └─ ●                   │ └─ ●
      │ │                        │
      │ └─── <empty>             └─── ●●●●●●●●●●
      │     ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
      └─────│●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●│
            └────────────────────────────────────────────────────────────────────────────────────────────────────┘
      
      move those items back to the 10s place (1 group in 100s becomes 10 groups in the 10s)
      
      0 10 0                      1 1
      │ │  │                      │ │
      │ │  └─ ●                   │ └─ ●
      │ │                         │
      │ └───┌──────────┐          └─── ●●●●●●●●●●
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     │●●●●●●●●●●│
      │     └──────────┘
      │
      └───── <empty>
      ```

  * borrow from 10s position: 10s position changes from 10 to 9

    ```
    0 10 0                      1 1
    │ │  │                      │ │
    │ │  └─ ●                   │ └─ ●
    │ │                         │
    │ └─── ●●●●●●●●●●           └─── ●●●●●●●●●●
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │     ┌──────────┐
    |     │●●●●●●●●●●│
    │     └──────────┘
    │
    └───── <empty>

        move those items back to the 1s place (1 group in 10s becomes 10 items in the 1s)

    0 9 10                     1 1
    │ │ │                      │ │
    │ │ └─┌─┐                  │ └─ ●
    │ │   │●│                  │
    │ │   │●│                  └─── ●●●●●●●●●●
    │ │   │●│
    │ │   │●│
    │ │   │●│
    │ │   │●│
    │ │   │●│
    │ │   │●│
    │ │   │●│
    │ │   │●│
    │ │   └─┘
    │ └─── ●●●●●●●●●●          
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●● 
    │      ●●●●●●●●●●
    │
    └───── <empty>
    ```

* subtract 1s position: 10-1 results in 9

* subtract 10s position: 9-1 results in 8

* subtract 100s position: 0-0 results in 0 (why? because 11 is the same as 011)

The way to perform this algorithm in real-life is to stack the two numbers being subtracted on top of each other, where the positions for both numbers match up (e.g. the 1s position matches up, the 10s position matches up, the 100s position matched up, etc..). Then, subtract the individual single digit components together (from right-to-left). Everytime borrowing is needed, cross out the number being changed and put the place their new numbers above. For example, subtracting 100 and 11 ...

```{define-block}
ktvertsub
ktvertsub_macro/
kthelper_code/target/appassembler/
```

```{ktvertsub}
{1}{0}{0}
{ }{1}{1}
------
{ }{ }{ }
```

* subtract 1s position: 0-1 not possible, borrow from 10s position

  * borrow from 10s position: can't borrow 10s position is 0, borrow from 100s position

    * borrow from 100s position: 100s position subtracts 1 (goes from 1 to 0), 10s position adds 10 (goes from 0 to 10)

      ```{ktvertsub}
      {0}{10}{ }
      {1}{ 0}{0}
      { }{ 1}{1}
      ------
      { }{  }{ }
      ```

  * borrow from 10s position: 10s subtracts 1 (goes from 10 to 9), 1s position adds 10 (goes from 0 to 10)

    ```{ktvertsub}
    { }{ 9}{  }
    {0}{10}{10}
    {1}{ 0}{ 0}
    { }{ 1}{ 1}
    ------
    { }{  }{  }
    ```

* subtract 1s position: 10-1 results in 9

  ```{ktvertsub}
  { }{ 9}{  }
  {0}{10}{10}
  {1}{ 0}{ 0}
  { }{ 1}{ 1}
  ------
  { }{  }{ 9}
  ```

* subtract 10s position: 9-1 results in 8

  ```{ktvertsub}
  { }{ 9}{  }
  {0}{10}{10}
  {1}{ 0}{ 0}
  { }{ 1}{ 1}
  ------
  { }{ 8}{ 9}
  ```

* subtract 100s position: 0-0 results in 0

  ```{ktvertsub}
  { }{ 9}{  }
  {0}{10}{10}
  {1}{ 0}{ 0}
  { }{ 1}{ 1}
  ------
  {0}{ 8}{ 9}
  ```

  ```{note}
  The number 11 has nothing in its 100s place -- nothing is the same as 0. 11 is the same as 011.
  ```

The way to perform this algorithm via code is as follows...

```{output}
wholenum_code/src/main/java/com/offbynull/wholenum/MainSubtraction.java
java
//MARKDOWN_ISOLATE\s*\n([\s\S]+)\n\s*//MARKDOWN_ISOLATE
```

```{define-block}
wholenumsub
wholenumsub_macro/
wholenum_code/target/appassembler/
```

```{wholenumsub}
100 11
```

# Whole Number Multiplication

`{bm} Multiplication` is the concept of taking a number and iteratively adding it to itself a certain number of iterations. For example, 3 added to itself for 5 iterations results in 15 items...

```
3+3+3+3+3=15

 [●●●] 3
 [●●●] 3
 [●●●] 3
 [●●●] 3
 [●●●] 3
```

Multiplication is typically represented using the infix operator \*. The above example would be represented as 3\*5. When written in formal math notation, it may also be written as...
 * `{kt} 3 \cdot 5`
 * `{kt} 3(5)`
 * `{kt} (3)5`

```{note}
Do not use x or a cross as a symbol for multiplication. It causes confusion for algebra expressions.
```

The output of a multiplication operation is called the `{bm} product`. In the example above, 15 is the product.

The inputs into the multiplication operation are either...
* called factors -- in the example above, 3 and 5 are the factors,
* or the first input is called the `{bm} multiplier` and the second input is called the `{bm} multiplicand` -- in the example above, 3 is the multiplier and 5 is the multiplicand.

```{note}
You can think of this as a function that takes in 2 arguments: mult(3, 5).
```

When using words, multiplication is typically represented using the following syntax:

* `{bm} multiply` -- e.g. multiply 3 and 5
* `{bm} multiplied` -- e.g. 3 multiplied by 5
* `{bm} times` -- e.g. 3 times 5
* `{bm} product of` -- e.g. the product of 3 and 5

```{note}
There are certain special words that denote multiplication. For example, the word `{bm} twice` means 2 multiplied by something else -- e.g. twice 5 is the same thing as 2*5.

Much less common is the word `{bm} thrice` -- it means 3 times something else. The pattern here seems to be the add "ice" to the end of the number? Unsure, but Google seems to give a definition for fourice.
```

Properties of multiplication:

 * Order in which 2 numbers are multiplied doesn't matter (commutative).
   
   ```
    3*5       vs     5*3
   ┌───┐            ┌┬┬┬┐
   ├●●●┤3           │●●●│
   ├●●●┤3           │●●●│
   ├●●●┤3           │●●●│
   ├●●●┤3           │●●●│
   ├●●●┤3           │●●●│
   └───┘            └┴┴┴┘
                     555

   the number of dots is the same
   ```

 * Any number multiplied by 0 is 0.

   This makes sense if you think of multiplication as iterative addition...

   ```{javascript}
   var product = 0;
   for (var i = 0; i < multiplicand; i++) {
       product += multiplier;
   }
   ```

   If you iterate 0 times, the product will be 0.

 * Any number multiplied by 1 results in that same number (identity).

   ```
   3*3=3+3+3
   3*2=3+3
   3*1=3 -- 3 is just by itself, it isn't being added
   ```

The algorithm used by humans to multiply large numbers together is called `{bm} vertical multiplication`. Vertical multiplication relies on three ideas...

1. Humans have the ability to multiply a single digit number to another single digit number through memorization. For example...

   * 3\*4 is 12 (3+3+3+3)
   * 1\*9 is 9  (9)
   * 9\*9 is 81 (9+9+9+9+9+9+9+9+9)

   ... are all multiplication operations that can be done quickly if the person has cached the table below into their memory.

   | *  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
   |----|----|----|----|----|----|----|----|----|----|----|
   | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |
   | 1  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
   | 2  | 0  | 2  | 4  | 6  | 8  | 10 | 12 | 14 | 16 | 18 |
   | 3  | 0  | 3  | 6  | 9  | 12 | 15 | 18 | 21 | 24 | 27 |
   | 4  | 0  | 4  | 8  | 12 | 15 | 20 | 24 | 28 | 32 | 36 |
   | 5  | 0  | 5  | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 |
   | 6  | 0  | 6  | 12 | 18 | 24 | 30 | 36 | 42 | 48 | 54 |
   | 7  | 0  | 7  | 14 | 21 | 28 | 35 | 42 | 49 | 56 | 63 |
   | 8  | 0  | 8  | 16 | 24 | 32 | 40 | 48 | 56 | 64 | 72 |
   | 9  | 0  | 9  | 18 | 27 | 36 | 45 | 54 | 63 | 72 | 81 |

2. Numbers represented in place-value notation can be broken down into single digit components -- the place of each digit in the number represents some portion of that number's value. For example, the number 935 can be broken down as 9 100s, 3 10s, and 5 1s...

   ```
   100
   100
   100
   100
   100            1
   100            1
   100     10     1
   100     10     1
   100     10     1
   ---     --     -
   900     30     5
   
   
   
   9 3 5
   │ │ │
   │ │ └─ ●
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │
   │ └─── ●●●●●●●●●●
   │      ●●●●●●●●●●
   │      ●●●●●●●●●●
   │
   └───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
   ```

3. If two numbers start with a single non-zero digit is followed by zero or more 0s, the result of their multiplication is equivalent to multiplying the single non-zero digits together and appending the 0s to the end. For example, ..

   * 30 \* 2 is 60 -- 3 ends in 1 zero and 2 ends in no zeros, so the result has 1 zero

     ```
     ┌─┬─┬─┐
     │●│●│●│
     ├─┼─┼─┤  3*2, each box has 1 item and there's 6 boxes -- 6 total items
     │●│●│●│       
     └─┴─┴─┘
  
     ┌──────────┬──────────┬──────────┐
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     ├──────────┼──────────┼──────────┤ 30*2, each box has 10 items and there's 6 boxes -- 60 total items
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│       
     └──────────┴──────────┴──────────┘
     ```

   * 3 \* 20 is 60 -- 3 ends in no zeros and 2 ends in 1 zero, so the result has 1 zero

     ```
     ┌─┬─┬─┐
     │●│●│●│
     ├─┼─┼─┤  3*2, each box has 1 item and there's 6 boxes -- 6 total items
     │●│●│●│       
     └─┴─┴─┘
  
     ┌─┬─┬─┐
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     ├─┼─┼─┤ 3 * 20, each box has 10 items and there's 6 boxes -- 60 total items
     │●│●│●│         
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     │●│●│●│
     └─┴─┴─┘
     ```

   * 30 \* 20 is 600 -- 30 ends in 1 zero and 20 ends in 1 zero, so the result has 2 zeros

     ```
     ┌─┬─┬─┐
     │●│●│●│
     ├─┼─┼─┤  3*2, each box has 1 item and there's 6 boxes -- 6 total items
     │●│●│●│       
     └─┴─┴─┘
  
     ┌──────────┬──────────┬──────────┐
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     ├──────────┼──────────┼──────────┤ 30 * 20, box has 100 items and there's 6 boxes -- 600 total items
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│           
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     │●●●●●●●●●●│●●●●●●●●●●│●●●●●●●●●●│
     └──────────┴──────────┴──────────┘
     ```

Any two numbers can be multiplied by ...
1. breaking down each number into its single digit components (idea 2 above),
2. then multiplying each component from the first number by each components from the second number (idea 1 and 3 above),
3. then adding the results of those multiplications.

For example, the number 43 and 2 are broken down as follows...

```
4 3                      2
│ │                      │
│ └─ ●                   └─ ●
│    ●                      ●         
│    ●               
│                        
└─── ●●●●●●●●●●          
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

 * 43 is 40 + 3 (4 in the 10s place / 3 in the 1s place)
 * 2 is 2 (2 in the 1s place)

Multiply their individual single digit components together results in ... 

 * 2\*3 results in 6 (see idea 1)
 * 2\*40 results in 80, because 2\*4 is 8 (see idea 1) and the zeros from numbers multiplied are appended to the result (see idea 3)

Add the results of the multiplications: 80 + 6 is 86. Note that 43 + 43 is also 86. Each multiplication above is giving back a portion of the final multiplication value, specifically a portion of a single digit component in the final multiplication value -- they need to be combined by adding.

```
8 6
│ │ ┌─┐
│ └─┤●│
│   │●│ 3        
│   │●│
│   ├─┤
│   │●│
│   │●│ 3
│   │●│
│   └─┘
│   ┌──────────┐
└───┤●●●●●●●●●●│          
    │●●●●●●●●●●│
    │●●●●●●●●●●│ 4
    │●●●●●●●●●●│
    ├──────────┤
    │●●●●●●●●●●│
    │●●●●●●●●●●│
    │●●●●●●●●●●│ 4
    │●●●●●●●●●●│
    └──────────┘
```

For another more complex example, the number 43 and 22 are broken down as follows...

```
4 3                      2 2
│ │                      │ │
│ └─ ●                   │ └─ ●
│    ●                   │    ●         
│    ●                   │              
│                        └─── ●●●●●●●●●●
└─── ●●●●●●●●●●               ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
     ●●●●●●●●●●
```

 * 43 is 40 + 3 (4 in the 10s place / 3 in the 1s place)
 * 22 is 20 + 2 (2 in the 10s place / 2 in the 1s place)

Multiply their individual single digit components together results in ... 

 * 2\*3 results in 6 (see idea 1)
 * 2\*40 results in 80, because 2\*4 is 8 (see idea 1) and the zeros from numbers multiplied are appended to the result (see idea 3)
 * 20\*3 results in 60, because 2\*3 is 6 (see idea 1) and the zeros from numbers multiplied are appended to the result (see idea 3)
 * 20\*40 results in 800, because 2\*4 is 8 (see idea 1) and the zeros from numbers multiplied are appended to the result (see idea 3)

Add the results of the multiplications: 800 + 60 + 80 + 6 is 946. Note that 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 + 43 is also 946. Each multiplication above is giving back a portion of the final multiplication value, specifically a portion of a single digit component in the final multiplication value -- they need to be combined by adding.

The way to perform this algorithm in real-life is to stack the two numbers being multiplied on top of each other, where the positions for both numbers match up (e.g. the 1s position matches up, the 10s position matches up, the 100s position matched up, etc..). For example...

```{define-block}
ktvertmul
ktvertmul_macro/
kthelper_code/target/appassembler/
```

```{ktvertmul}
{ }{4}{3}
{ }{2}{2}
-----
{ }{ }{ }
```

Then, for each component in the bottom number (from right-to-left), isolate to its single digit component and multiply by each component in the top number (from right-to-left). The answer for each digit of the bottom row is written underneath the answer prior to it. Starting from the first component of the bottom number...

 * Isolate to 2 (bottom) and 3 (top), resulting in 6.

   ```{ktvertmul}
   { }        {4}        {\green{3}}
   { }        {2}        {\green{2}}
   -----
   { }        { }        {\green{6}}
   ```

 * Isolate to 2 (bottom) and 40 (top), resulting in 80. Only the 8 needs to be written because this is effectively the same as doing 40\*2 (80) then adding the 6 from the 3\*2 prior --  80+6 is 86.

   ```{ktvertmul}
   { }        {\green{4}}{3}
   { }        {2}        {\green{2}}
   -----
   { }        {\green{8}}{6}
   ```

 * Isolate to 20 (bottom) and 3 (top), resulting in 60.

   ```{ktvertmul}
   { }        {4}        {\green{3}}
   { }        {\green{2}}{2}
   -----
   { }        {8}        {6}
   { }        {\green{6}}{\green{0}}
   ```

 * Isolate to 20 (bottom) and 40 (top), resulting in 800. Only the 8 needs to be written because this is effectively the same as doing 40\*20 (800) then adding the 60 from the 3\*20 prior --  800+60 is 860.

   ```{ktvertmul}
   { }        {\green{4}}{3}
   { }        {\green{2}}{2}
   -----
   { }        {8}        {6}
   {\green{8}}{6}        {0}
   ```

Then, add the the answers from each bottom iteration to get the final answer...

```{ktvertmul}
{ }        {4}        {3}
{ }        {2}        {2}
-----
{ }        {8}        {6}
{8}        {6}        {0}
-----
{\green{9}}{\green{4}}{\green{6}}
```

In many cases, multiplying 2 individual single digit components results in an extra digit (e.g. 7\*7=49). If this happens, the bleed over digit is carried over to the next position (on the left). That is, the bleed over digit will get added to the result of the multiplication in the next position. This is denoted by stacking the bleed over digit on top of the next position. For example...

```{ktvertmul}
{ }{7}{7}
{ }{7}{7}
-----
{ }{ }{ }
```

 * Isolate to 7 (bottom) and 7 (top), resulting in 49. The 9 is kept and 40 carries over to the next position.

   ```{ktvertmul}
   { }        {\green{4}}        { }
   { }                {7}{\green{7}}
   { }                {8}{\green{7}}
   -----
   { }                { }{\green{9}}
   ```

 * Isolate to 7 (bottom) and 70 (top), resulting in 490. Add the 40 from the carry-over to make it 530. Only the 53 needs to be written because this is effectively the same as having 530 then adding the 9 from the 7\*7 prior --  530+9 is 539.

   ```{ktvertmul}
   { }        {\green{4}}        { }
   { }        {\green{7}}        {7}
   { }                {8}{\green{7}}
   -----
   {\green{5}}{\green{3}}        {9}
   ```

 * Isolate to 80 (bottom) and 7 (top), resulting in 560. The 60 is kept and 500 carries over to the next position.

   ```{ktvertmul}
   { }        {\green{5}}        { }
   { }                {4}        { }
   { }                {7}{\green{7}}
   { }        {\green{8}}        {7}
   -----
   {5}        {3}        {9}
   { }        {\green{6}}{\green{0}}
   ```

 * Isolate to 80 (bottom) and 70 (top), resulting in 5600. Add the 500 from the carry-over to make it 6100. Only the 61 needs to be written because this is effectively the same as having 6100 then adding the 60 from the 80\*7 prior --  6100+60 is 6160.

   ```{ktvertmul}
   { }                { }{\green{5}}        { }
   { }                { }        {4}        { }
   { }                { }{\green{7}}        {7}
   { }                { }{\green{8}}        {7}
   -----
   { }                {5}        {3}        {9}
   {\green{6}}{\green{1}}        {6}        {0}
   ```

Then, add the the answers from each bottom iteration to get the final answer...

   ```{ktvertmul}
   { }                { }        {5}        { }
   { }                { }        {4}        { }
   { }                { }        {7}        {7}
   { }                { }        {8}        {7}
   -----
   { }                {5}        {3}        {9}
   {\green{6}}{\green{1}}        {6}        {0}
   -----
   {\green{6}}{\green{6}}{\green{9}}{\green{9}}
   ```

The way to perform this algorithm via code is as follows...

```{output}
wholenum_code/src/main/java/com/offbynull/wholenum/MainMultiplication.java
java
//MARKDOWN_ISOLATE\s*\n([\s\S]+)\n\s*//MARKDOWN_ISOLATE
```

```{define-block}
wholenummul
wholenummul_macro/
wholenum_code/target/appassembler/
```

```{wholenummul}
77 87
```

# Whole Number Division

`{bm} Division` is the concept of taking a number and iteratively subtracting it by another number to find out how many iterations it can be subtracted. For example, 15 can be subtracted by 3 exactly 5 iterations before nothing's left...

```
 [●●●●●●●●●●●●●●●] start with 15

 [●●●●●●●●●●●●] 15-3 is 12 (iteration 1)
 [●●●●●●●●●] 12-3 is 9 (iteration 2)
 [●●●●●●] 9-3 is 6 (iteration 3)
 [●●●] 6-3 is 3 (iteration 4)
 [] 3-3 is 0 (iteration 5)
```

Another way of thinking about division is that it's chopping up a number. Imagine cutting up a pie into 15 pieces and eating 3 pieces at a time. The pie will be done after you've eaten 5 times.


```{diagramhelperfrac}
radius 40
12
15
```

```{diagramhelperfrac}
radius 40
9
15
```

```{diagramhelperfrac}
radius 40
6
15
```

```{diagramhelperfrac}
radius 40
3
15
```

```{diagramhelperfrac}
radius 40
0
15
```

In certain cases, division may result in some remaining value that isn't large enough for another subtraction iteration to take place. This remaining value is called the `{bm} remainder` For example, 16 can be subtracted by 3 for 5 iterations but will have a remainder of 1...

```
 [●●●●●●●●●●●●●●●●] start with 16

 [●●●●●●●●●●●●●] 16-3 is 13 (iteration 1)
 [●●●●●●●●●●] 13-3 is 10 (iteration 2)
 [●●●●●●●] 10-3 is 7 (iteration 3)
 [●●●●] 7-3 is 4 (iteration 4)
 [●] 4-3 is 1 (iteration 5)

 only 1 item left -- not enough for another subtraction iteration
 
 1 is the remainder
```

```{note}
If a division operation results in no remainder, it's said to be divisible.
```

Division is typically represented using the infix operator / or ÷. The above example would be represented as 15/3 or 15÷3. It may also be written as `{kt} \frac{15}{3}`, which is just a fancier way of writing 15/3.

The output of a division operation is called the `{bm} quotient`. In the example above, the quotient is 5 (it subtracts 5 times).

The inputs into the division operation are called the `{bm} dividend` and `{bm} divisor`. In the example above, 15 is the dividend and 3 is the divisor.

* `{kt} dividend \div divisor = quotient`
* `{kt} dividend / divisor = quotient`
* `{kt} \frac{dividend}{divisor} = quotient`

```{note}
One way to think of this is that the dividend (the number on the left / top) is the starting value, and the divisor is the number being iteratively subtracted.

The quotient is the number of times you can subtract.
```

When using words, division is typically represented using the following syntax:

* `{bm} divide` -- e.g. divide 3 by 15
* `{bm} divided by/(divided by|divide by)/i` -- e.g. 3 divided by 15
* `{bm} divided into` -- e.g. 15 divided into 3
* `{bm} quotient of` -- e.g. the quotient of 3 and 15

```{note}
There are certain special words that denote division. For example, the word ...
* `{bm} half` means something divided by 2 -- e.g. half of 10 is the same as 10/2.
* `{bm} quarter` means something divided by 4 -- e.g. a quarter of 10 is the same 10/4.
```

Properties of division:

 * Any number divided by 1 results in the same number (identity).

   ```
   [●●●●●] start with 5
  
   [●●●●] 5-1 is 4 (iteration 1)
   [●●●] 4-1 is 3 (iteration 2)
   [●●] 3-1 is 2 (iteration 3)
   [●] 2-1 is 1 (iteration 4)
   [] 1-1 is 0 (iteration 5)
  
   5 iterations total
   ```

 * Any number divided by itself is 1.

   ```
   [●●●●●] start with 5
  
   [] 5-5 is 0 (iteration 1)
  
   1 iteration total
   ```

 * Any number divided by 0 is infinity.

   This makes sense if you think of division as iterative subtraction...

   ```{javascript}
   var quotient = 0;
   while (dividend >= divisor) {
       dividend -= divisor;
       quotient += 1;
   }
   ```

   This will iterate forever if the divisor is 0 because the dividend would never become less than the divisor -- the loop wouldn't terminate.

   ```{note}
   Another way to think of this is that division is the inverse of multiplication (it undoes multiplication). If it were the case that 10/0=?, then ?\*0=10. We know that this can't be the case because ?\*0=0.
   ```

The algorithm used by humans to divide large numbers is called `{bm} long division`. Long division relies on three ideas...

1. Numbers represented in place-value notation can be broken down into single digit components -- the place of each digit in the number represents some portion of that number's value. For example, the number 935 can be broken down as 9 100s, 3 10s, and 5 1s...

   ```
   100
   100
   100
   100
   100            1
   100            1
   100     10     1
   100     10     1
   100     10     1
   ---     --     -
   900     30     5
   
   
   
   9 3 5
   │ │ │
   │ │ └─ ●
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │    ● 
   │ │
   │ └─── ●●●●●●●●●●
   │      ●●●●●●●●●●
   │      ●●●●●●●●●●
   │
   └───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
          ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
   ```

2. If two numbers both end in the same number of 0s, dividing them is essentially the same as dividing them without their common 0 suffix. For example...

   * 45/5 = 9
   * 450/50 = 9
   * 4500/500 = 9
   * 45000/5000 = 9

   If both the dividend and the divisor end in 0s but the dividend has more 0s, dividing them is the essentially the same as dividing them without their 0 suffixes and then appending the difference of 0s to the suffix of the quotient. For example...

   * 45000/500 = 90
   * 45000/50 = 900
   * 45000/5 = 9000

3. Humans have the ability to...
   * add large numbers together via vertical addition.
   * subtract large numbers from each other via vertical subtraction.
   * multiply large numbers together via vertical multiplication.








TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED

TODO: THIS IS AN AWFUL EXPLAINATION AND NEEDS TO BE FIXED



The intuition behind dividing up a big number is that numbers can be broken down into their individual components (idea 1). The broken down values are easier to divide because components have trailing 0s (idea 2). For example, dividing the number 42 by 3.

```
42 = 40+2
   = (4*10) + 2

40: 4*10/3 --> 4/3*10 --> (1 R1)*10 --> 10 R10

Add remainder to next component and do again...

2: 10+2 --> 12/3 --> 4

Add quotients for each component 10+4=14

```

A number can be divided by ...
1. break down its divisor into single digit components (idea 1) above,
2. then iteratively dividing each of those single digit components by the dividend, carrying over the remainder to the next division (ideas 2 and 3 above).

For example, the divisor in 43212/12 can be broken down into the following single digit components:

 * 40000
 * 3000
 * 200
 * 10
 * 2

40000+3000+200+10+2=43212

From largest to the smallest component, divide.

40000 component
* `{kt} \frac{40000}{12} = 3000R4000`
* `{kt} \frac{4000}{12} = 300R400`
* `{kt} \frac{400}{12} = 30R40`
* `{kt} \frac{40}{12} = 3R4`
* 3333

3000 component
* `{kt} \frac{3000}{12} = 200R600`
* `{kt} \frac{600}{12} = 50R0`
* 250

200 component
* `{kt} \frac{200}{12} = 10R80`
* `{kt} \frac{80}{12} = 6R8`
* 16

10 component
* `{kt} \frac{10}{12} = 0R10`
* 0

2 component
* `{kt} \frac{2}{12} = 0R2`
* 0

Add up the quotients and the remainder value.
* Quotient: 3333+250+16+0=3599
* Remainder: 4+0+10+8+2=24

The remainder isn't less than 12 (divisor), so do the entire process again on the remainder.

24 can be broken down in to the following single digit components:

 * 20
 * 4

20 component
* `{kt} \frac{20}{12} = 1R8`
* 1

4 component
* `{kt} \frac{4}{12} = 0R4`
* 0

Add up the quotients and the remainder value.
* Quotient: 1+0=1
* Remainder: 8+4=12

The remainder the divisor, so add an extra notch ot the quotient and remove the remainder.
* Quotient: 1
* Remainder: 0

Now, add up all the quotients to get the final quotient and take the last remainder to get the final remainder.

Final quotient: 3599+1+1 = 3601 / Final remainder: 0.

 TODO: CONTINUE HERE CONTINUE HERE CONTINUE HERE

```{define-block}
ktlongdiv
ktlongdiv_macro/
kthelper_code/target/appassembler/
```

```{ktlongdiv}
{quotient}
{divisor}{dividend}
{line1}
{line2}
{line3}
```

```{ktlongdiv}
{047.9}
{5}{239.5}
{\underline{0}}
{23}
{\underline{20}}
{\phantom{0}39}
{\phantom{0}\underline{35}}
{\phantom{00}4\phantom{.}5}
{\phantom{00}\underline{4\phantom{.}5}}
{\phantom{004.}0}
```


# Multiple

To say that m is a `{bm} multiple` of n means that some integer exists such that when you multiply it by n you get m:- `{kt} n \cdot ? = m`. Typically both n and m are also integers.

For example, the multiples of 2 are...

* 2*0=2 -- 0 is a multiple of 2

* 2*1=2 -- 2 is a multiple of 2

  ```
  ┌──┐
  │●●│ 2 can be grouped as 1 group of 2
  └──┘
  ```

* 2*2=4 -- 4 is a multiple of 2

  ```
  ┌──┬──┐
  │●●│●●│ 4 can be grouped as 2 groups of 2
  └──┴──┘
  ```

* 2*3=6 -- 6 is a multiple of 2

  ```
  ┌──┬──┬──┐
  │●●│●●│●●│ 6 can be grouped as 3 groups of 2
  └──┴──┴──┘
  ```

* 2*4=8 -- 8 is a multiple of 2

  ```
  ┌──┬──┬──┬──┐
  │●●│●●│●●│●●│ 8 can be grouped as 4 groups of 2
  └──┴──┴──┴──┘
  ```

* etc..

A number like 7 wouldn't be a multiple of 2 because there is no integer that can be multiplied by 2 to get 7 -- 2\*3.5=7, but 3.5 isn't an integer.

```
┌──┬──┬──┬─┐
│●●│●●│●●│●│ 7 can't be grouped as groups of 2 (last group only has 1)
└──┴──┴──┴─┘
```

```{note}
See divisible section.
```

# Divisible

To say that m is `{bm} divisible` by n means that an integer results from dividing m by n: `{kt} m \div n = ?`. Typically both m and n are also integers, with the exception that n can't be 0 (can't divide by 0).

For example, 8 is divisible by...

* 8/1=8 -- 8 is divisible by 1

  ```
  ┌────────┐
  │●●●●●●●●│ 8 can be grouped as 1 group of 8
  └────────┘
  ```

* 8/2=4 -- 8 is divisible by 2

  ```
  ┌────┬────┐
  │●●●●│●●●●│ 8 can be grouped as 2 groups of 4
  └────┴────┘
  ```

* 8/4=2 -- 8 is divisible by 4

  ```
  ┌──┬──┬──┬──┐
  │●●│●●│●●│●●│ 8 can be grouped as 4 groups of 2
  └──┴──┴──┴──┘
  ```

* 8/8=1 -- 8 is divisible by 8

  ```
  ┌─┬─┬─┬─┬─┬─┬─┬─┐
  │●│●│●│●│●│●│●│●│ 8 can be grouped as 8 groups of 1
  └─┴─┴─┴─┴─┴─┴─┴─┘
  ```

In all of the above cases, the quotient is an integer -- it doesn't have a remainder. 8 wouldn't be divisible by a number like 3 because the result wouldn't be an integer. 8/3=2.6667, but 2.6667 isn't an integer.

```
┌───┬───┬──┐
│●●●│●●●│●●│ 8 can't be grouped as groups of 3 (last group only has 2)
└───┴───┴──┘
```

```{note}
The phrases `{bm} evenly divisible`, `{bm} evenly divide`s and divisible all mean the same thing.

The phrase `{bm} evenly divides into` is the same as `{bm} divides into` but that it doesn't have a remainder (whole). 4 divides into 8 (4/8=2), but 6 doesn't divide into 8 (6/8=0.75).
```

```{note}
Divisible and multiple refer to the same idea. Saying that 275 is a multiple of 5 (`{kt} 5\cdot?=275`) is the same as saying 275 is divisible by 5 (`{kt} 275\div5=?`).
```


`{bm} Common divisibility test`s are simple tests you can do on a number to see if its divisible. To see if a number is divisible by...

 * 2, check if the last digit is either 0, 2, 4, 6, or 8.

   |        |        |        |        |        |        |        |        |        |        |
   | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
   |   1    | **2**  |   3    | **4**  |   5    | **6**  |   7    | **8**  |   9    | **10** |
   |   11   | **12** |   13   | **14** |   15   | **16** |   17   | **18** |   19   | **20** |
   |   21   | **22** |   23   | **24** |   25   | **26** |   27   | **28** |   29   | **30** |
   |   31   | **32** |   33   | **34** |   35   | **36** |   37   | **38** |   39   | **40** |
   |   41   | **42** |   43   | **44** |   45   | **46** |   47   | **48** |   49   | **50** |

 * 5, check if the last digit is either 5 or 0.

   |        |        |        |        |        |        |        |        |        |        |
   | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
   |   1    |   2    |   3    |   4    | **5**  |   6    |   7    |   8    |   9    | **10** |
   |   11   |   12   |   13   |   14   | **15** |   16   |   17   |   18   |   19   | **20** |
   |   21   |   22   |   23   |   24   | **25** |   26   |   27   |   28   |   29   | **30** |
   |   31   |   32   |   33   |   34   | **35** |   36   |   37   |   38   |   39   | **40** |
   |   41   |   42   |   43   |   44   | **45** |   46   |   47   |   48   |   49   | **50** |

 * 10, check if the last digit is 0.

   |        |        |        |        |        |        |        |        |        |        |
   | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
   |   1    |   2    |   3    |   4    |   5    |   6    |   7    |   8    |   9    | **10** |
   |   11   |   12   |   13   |   14   |   15   |   16   |   17   |   18   |   19   | **20** |
   |   21   |   22   |   23   |   24   |   25   |   26   |   27   |   28   |   29   | **30** |
   |   31   |   32   |   33   |   34   |   35   |   36   |   37   |   38   |   39   | **40** |
   |   41   |   42   |   43   |   44   |   45   |   46   |   47   |   48   |   49   | **50** | 

 * 3, sum up the individual digits and check if divisibly by 3.

   This is a recursive operation. For example...
   * 6
     * 6 is a multiple of 3
   * 36363,
     * 3+6+3+6+3=21,
       * 2+1=3
         * 3 is a multiple of 3

   Keep doing it until you get a 1 digit answer and check to see if that answer is either 3, 6, or 9.

   |        |        |        |        |        |        |        |        |        |        |
   | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
   |   1    |   2    | **3**  |   4    |   5    | **6**  |   7    |   8    | **9**  |   10   |
   |   11   | **12** |   13   |   14   | **15** |   16   |   17   | **18** |   19   |   20   |
   | **21** |   22   |   23   | **24** |   25   |   26   | **27** |   28   |   29   | **30** |
   |   31   |   32   | **33** |   34   |   35   | **36** |   37   |   38   | **39** |   40   |
   |   41   | **42** |   43   |   44   | **45** |   46   |   47   | **48** |   49   |   50   |
   | **51** |   52   |   53   | **54** |   55   |   56   | **57** |   58   |   59   | **60** |

 * 6, apply common divisibility tests for 2 and 3, they both must pass.

   |        |        |        |        |        |        |        |        |        |        |
   | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
   |   1    |   2    |   3    |   4    |   5    | **6**  |   7    |   8    |   9    |   10   |
   |   11   | **12** |   13   |   14   |   15   |   16   |   17   | **18** |   19   |   20   |
   |   21   |   22   |   23   | **24** |   25   |   26   |   27   |   28   |   29   | **30** |
   |   31   |   32   |   33   |   34   |   35   | **36** |   37   |   38   |   39   |   40   |
   |   41   | **42** |   43   |   44   |   45   |   46   |   47   | **48** |   49   |   50   |
   |   51   |   52   |   53   | **54** |   55   |   56   |   57   |   58   |   59   | **60** |

   ```{note}
   The bold numbers in the table above are numbers that appear bold in both the table for 2s and the table for 3s -- they must be bold in both tables.
   ```

# Factor

Let's say you have an integer number. The `{bm} factor`s of that number are the integers you can multiply together to get that number...

```java
int myNumber = ...;
int factor1 = ...;
int factor2 = ...;
if (factor1 * factor2 == myNumber) {
    System.out.println(factor1 + " and " + factor2 + " are factors of " + myNumber);
} 
```

For example, the factors of 32 are...

* 32=32\*1 -- 32 and 1 are factors
* 32=16\*2 -- 16 and 2 are factors
* 32=8\*4 -- 8 and 4 are factors
* 32=4\*8 -- 4 and 8 are factors
* 32=2\*16 -- 2 and 16 are factors
* 32=1\*32 -- 1 and 32 are factors

... 1, 2, 4, 8, 16, and 32.

```{note}
Shouldn't negative integers also be a factor? e.g. 32=-1*-32. It turns out that for positive integers, negative factors aren't included? For negative integers, they are. Factoring negative integers is discussed further below in this section.

See https://math.stackexchange.com/a/404789
```

The factors for any number will always be between 1 and that number (inclusive). A naive algorithm for finding the factors of any number would be to have a nested loop exhaustively check integers to see which are factors...

```{output}
factor_code/src/main/java/com/offbynull/factor/FactorNaive.java
java
//MARKDOWN_ISOLATE\s*\n([\s\S]+)\n\s*//MARKDOWN_ISOLATE
```

```{define-block}
factornaive
factornaive_macro/
factor_code/target/appassembler/
```

```{factornaive}
32
```

We can take advantage of the fact that division is the inverse of multiplication to optimize the algorithm above. The code below loops over each possible factor once, using it to calculate what the other factor would be and then checking it to make sure it's valid...

```{output}
factor_code/src/main/java/com/offbynull/factor/FactorFast.java
java
//MARKDOWN_ISOLATE\s*\n([\s\S]+)\n\s*//MARKDOWN_ISOLATE
```

```{define-block}
factorfast
factorfast_macro/
factor_code/target/appassembler/
```

```{factorfast}
32
```

The optimized algorithm above can be even further optimized by making it skip over calculations that give back repeat factors. As `factor1` increases, `factor2` decreases. Once `factor1 => factor2`, each is basically walking into domains the other was just in (they're each going to walk over integers the other already walked over). There's no point in continuing any further because the factors calculated past that point will just be duplicates of those prior. For example, when calculating the factors of 32...

* 32/1=32 -- 1 and 32 are factors
* 32/2=16 -- 2 and 16 are factors
* ~~32/3=10.666~~
* 32/4=8 -- 4 and 8 are factors
* ~~32/5=6.4~~
* ~~32/6=5.333~~ <-- Stop here because 6 >= 5.333

Any factors calculated past `factor1 => factor2` will be duplicates of factors that were already walked over... 

* 32\*1 = 1\*32 = 32 -- 32 and 1 are factors.
* 16\*2 = 2\*16 = 32 -- 16 and 2 are factors.
* 8\*4 = 4\*8 = 32 -- 8 and 4 are factors.

```{output}
factor_code/src/main/java/com/offbynull/factor/FactorFastest.java
java
//MARKDOWN_ISOLATE\s*\n([\s\S]+)\n\s*//MARKDOWN_ISOLATE
```

```{define-block}
factorfastest
factorfastest_macro/
factor_code/target/appassembler/
```

```{factorfastest}
32
```

There are 2 special cases when dealing with factors...

The first is that all numbers are a factor of 0 (e.g. 0\*5=0, 0\*9999=0).

The second is that if the number were a negative integer, the factors would include negative numbers as well. For example, the factors of -8 are...

* -8=8\*-1 -- 8 and -1 are factors
* -8=4\*-2 -- 4 and -2 are factors
* -8=2\*-4 -- 2 and -4 are factors
* -8=1\*-8 -- 1 and -8 are factors
* -8=-1\*8 -- -1 and 8 are factors
* -8=-2\*4 -- -2 and 4 are factors
* -8=-4\*2 -- -4 and 2 are factors
* -8=-8\*1 -- -8 and 1 are factors

... -8, -4, -2, -1, 1, 2, 4, 8.

# Prime

A counting number with only 2 factors is called a `{bm} prime` number. That is, if a counting number is only divisible by 1 and it itself, it's a prime number. Examples of prime numbers: 2, 3, 5, 7, 11, 13, 17, and 19.

A counting number with more than 2 factors is called a `{bm} composite` number. Examples of composite numbers: 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, and 20.

```{note}
The number 1 is neither a prime number nor a composite number. 1's only factor is itself: 1\*1=1. Prime numbers need 2 factors and composite numbers need more than 2 factors.
```

# Algebra

`{bm} Algebra` is the study of mathematical operations and the rules for manipulating those operations.

Common mathematical operations:

* Addition -- denoted by +, e.g. 5+4
* Subtraction -- denoted by -, e.g. 5-4
* Multiplication -- denoted by a center dot or brackets, e.g. 5(4), (4)5, or 4·5
* Division -- denoted by / or as a fraction, e.g. ½ or `{kt} \frac{1}{2}`
* Exponent -- denoted by superscript, e.g. `{kt} 8^2`

These operations can typically be chained together. One or more operations combined together is called an `{bm} expression`. For example, `{kt} 4 + 3 * 5` is an expression.

The operations in an expression can make use of either constants or variables. A...
 * `{bm} variable` is a placeholder that can be replaced with a number, typically represented as a letter.
 * `{bm} constant` is a number.

For example, the expression `{kt} x + 3 * x` has the constant 3 and the variable x. Note that the variable x is used 2 times in the expression -- when its set to a number, both instances of x in the expression must change to that number. For example, if x were set to 5, the expression would be `{kt} 5 + 3 * 5`.

TODO: BEDMAS

To `{bm} simplify` an expression is to perform all the math operations possible on the expression. For example, in `{kt} 5+3*5`, first the multiplication gets performed to make the expression `{kt} 5+15`, then the addition gets performed to make the expression `{kt} 20`.

To `{bm} evaluate` an expression is to (replace) set all of its variables to numbers and perform all the operations. In other words, set all variables to a number and simplify the expression.

`{bm-ignore} terminology`

In an expression, the word...
 * `{bm} term` means a constant or a product of a constant and one or more variables. For example, ...
   * x
   * 5x
   * 5xy
   * 5x^2
 * `{bm} coefficient` means a constant that multiplies variables in a term. For example, in the term...
   * 9a, 9 is the coefficient
   * y, 1 is the coefficient because 1 is implied (y = 1y)
   * 5x^2, 5 is the coefficient

```{note}
The book states that the term 7 has a coefficient of 7, but this doesn't mesh with the description that the book gives for coefficients -- "The constant that multiplies the variable(s) in a term is called the coefficient." Other sources seem to corroborate that a constant by itself doesn't equality as a coefficient: https://www.youtube.com/watch?v=uiIg6ADVz8c.
```

2 terms are considered `{bm} like term/(like term|like-term)/i`s if they either...
 * have the same variable to the power of the same exponent.
   * e.g. 7x and 10x  (x is the same as x^1)
   * e.g. 55a^4 and a^4
   * e.g. 2^(b+1) and 7^(b+1)
 * are both constants.
   * e.g. 5 and 7
   * e.g. 6 and 909

Like terms can be combined together by adding the coefficients. For example, 4x+2x can be simplified to 6x. The reason for this is that multiplication is just iterative addition -- it becomes apparent once 4x and 2x get broken down as addition in the expression ...

```
       4x         2x
┌─────────────┐ ┌─────┐
 x + x + x + x + x + x
└─────────────────────┘
          7x
```

```{note}
If multiple additions are being chained together, often times its helpful to re-order it so that like terms are together -- it makes it easier to combine like terms. You can do this because of the commutative property of addition. For example..

5x^2 + 3y + 4x^2 + 2y can be re-order as 5x^2 + 4x^2 + 3y + 2y
```

When 2 expressions evaluate to the same result, they can be written as an equation. An `{bm} equation` is denoted by a =, where the left-side is one expression and the right-side is another. For example, `{kt} 5x = 30`.

To `{bm} solve` an equation means to determine the values of the variables in the equation such that both sides evaluate to the same number. This is done by applying the various rules of the operations used in the expressions of the equation. For example, solving `{kt} 5x = 30`...
* `{kt} 5x = 30`
* `{kt} \frac{5x}{5} = \frac{30}{5}`
* `{kt} 1x = 6`
* `{kt} x = 6`

 The set of variable to number mappings for an equation is called a `{bm} solution` -- `{kt} x=6` is the solution of the equation.

TODO: write section on converting words to algebra / algebra to words (see "Translate Words to Algebraic Expressions" in chapter 2.2) -- write a solver for this and make sure it handles complex expressions (e.g. nine times five less than twice x = 2x-(9*5))






Algebraic terminology:

 * A variable is a placeholder that can be replaced with a number, typically represented as a letter.
 * A constant is a number.
 * A expression is a set of mathematical operations performed on constants and variables. For example, 5 + 3 * x is an expression.
 * A equation is 2 expressions that are equal to each other

Algebraic notation:

* `{kt} a=b` -- a equals b

  When both sides represent the same value, it's said that they're equal.

* `{kt} a \neq b` - a NOT equals b

  When both sides represent different value, it's said that they're not equal.

* `{kt} a > b` -- greater than

  When the value of left-side is more than the right-side, the left is said to be greater than the right.

  ```{note}
  This is the same as `{kt} b < a`. Think of the symbol as a mouth. The mouth is trying trying to eat the larger value -- it's open in that direction.
  ```
* `{kt} a < b` -- less than

  When the value of left-side is less than the right-side, the left is said to be greater than the right.

  ```{note}
  This is the same as `{kt} b > a`.  Think of the symbol as a mouth. The mouth is trying trying to eat the larger value -- it's open in that direction.
  ```

* `{kt} a \geq b` -- greater than or equal

  When the value of left-side is more than OR equal to the right-side, the left is said to be greater than the right.

* `{kt} a \leq b` -- less than or equal

  When the value of left-side is less than OR equal to the right-side, the left is said to be greater than the right.

KEEP WORKING ON THESE:
ADD FRACTION ADDING AND MULTIPLICATION RULES (recipriocals, cross multiply, etc..)
ADD REMAINING ALGEBRA RULES
https://en.wikiversity.org/wiki/Algebraic_Properties_of_Equality
https://en.wikiversity.org/wiki/Basic_Laws_of_Algebra
http://www.themathpage.com/aPreCalc/algebraPre.htm (specifically 1, 6, and 7?)
ADD TRIVIAL AND NON-TRIVIAL EXAMPLES


TODO: write section about converting expressions to phrases and vice versa

## Order of Operations

The `{bm} order of operations` are as follows:

1. Brackets
1. Exponents
1. Division and Multiplication (evaluated left-to-right)
1. Addition and Subtraction (evaluated left-to-right)

These rules are often abbreviated as either...

* `{bm} BEDMAS` - Brackets / Exponents / Division and Multiplication / Addition and Subtraction
* `{bm} PEMDAS` - Parenthesis / Exponents / Multiplication and Division / Addition and Subtraction (can be remembered as Please Excuse My Dear Aunt Sally)

Note that these 2 are essentially the same. Division and multiplication are swapped, but since division and multiplication are evaluated left-to-right in the same step, it makes no difference.

## Operation Rules

TODO: talk about inverse of an operation, properties such as commutatitive, etc.. and make sure to properly bookmark them so they can be referenced from the neighbouring equality rules section below. move the stuff below into its relevant subsections

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

### Addition

inverse of addition is subtraction

### Subtraction

inverse of subtraction is addition

### Multiplication

inverse of division

### Division

inverse of multiplication

## Equality Rules

TODO: talk about how you can subtract/add/multiply/divide anything so long as you do it to both sides... e.g. x=5 add y to both sides to get x+y=5+y, x+y=5+y subtract y from both sides to get

using a balancing scale might be a good way to represent this -- if it's already balanced, adding 5 apples to one side means you have to add 5 apples to the other side to keep it balanced

starts at section 2.3

see subtraction property of equality

see addition property of equality

see division property of equality

see multiplciation property of equality

ALSO, section 2.3 talks about converting phrases to equations and viceversa -- implement this (see "Translate Word Phrases to Algebraic Equations" section)... words that map to equality...

* `{bm} is equal to` -- e.g. x is equal to 1
* `{bm} equals` -- e.g. x equals 1
* `{bm} is the same as` -- e.g. x is the same as 1
* `{bm} is` -- e.g. x is 1
* `{bm} gives` -- e.g. ???
* `{bm} was` -- e.g. x was 1
* `{bm} will be` -- e.g. x will be 1

some of the above are overkill and need to be pruned

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

__EXERCISE__

1.2.59) five plus two

1.2.60) six plus three

1.2.61) thirteen plus eighteen

1.2.62) fifteen plus sixteen

1.2.63) two hundred fourteen plus six hundred forty two

1.2.64) four hundred thirty eight plus one hundred thirteen

1.2.65) model 2 + 4...

```
□□ □□□□
2   4
```

1.2.66) model 5 + 3...

```
□□□□□ □□□
  5    3
```

1.2.67) model 8 + 4...

```
□□□□□□□□ □□□
    8     4
```

1.2.68) model 5 + 9...

```
□□□□□ □□□□□□□□□
   5      9
```

1.2.69) model 14 + 75...

```
□□□□□□□□□□    □□□□□□□□□□
   □□□□       □□□□□□□□□□
    14        □□□□□□□□□□
              □□□□□□□□□□
              □□□□□□□□□□
              □□□□□□□□□□
              □□□□□□□□□□
                □□□□□
                 75
```

1.2.70) model 15 + 63...

```
□□□□□□□□□□    □□□□□□□□□□
  □□□□□       □□□□□□□□□□
   15         □□□□□□□□□□
              □□□□□□□□□□
              □□□□□□□□□□
              □□□□□□□□□□
                 □□□
                 63
```

1.2.71) model 16 + 25...

```
□□□□□□□□□□    □□□□□□□□□□
  □□□□□□      □□□□□□□□□□
    16          □□□□□
                 25
```

1.2.72) model 14 + 27...

```
□□□□□□□□□□    □□□□□□□□□□
   □□□□       □□□□□□□□□□
    14         □□□□□□□
                 27
```

1.2.73) Missing blocks filled in...

| +  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 0  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| 1  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
| 2  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 |
| 3  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 |
| 4  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 |
| 5  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 |
| 6  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 |
| 7  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| 8  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 15 | 16 |
| 9  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |

1.2.74) Missing blocks filled in...

| +  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 0  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| 1  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
| 2  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 |
| 3  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 |
| 4  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 |
| 5  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 |
| 6  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 |
| 7  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| 8  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 15 | 16 |
| 9  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |

1.2.75) Missing blocks filled in...

| +  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| -- | -- | -- | -- | -- | -- | -- | -- |
| 6  | 6  | 7  | 8  | 9  | 10 | 11 | 12 |
| 7  | 7  | 8  | 9  | 10 | 11 | 12 | 13 |
| 8  | 8  | 9  | 10 | 11 | 12 | 13 | 14 |
| 9  | 9  | 10 | 11 | 12 | 13 | 14 | 15 |

1.2.76) Missing blocks filled in...

| +  | 6  | 7  | 8  | 9  |
| -- | -- | -- | -- | -- |
| 3  | 6  | 7  | 8  | 9  |
| 4  | 7  | 8  | 9  | 10 |
| 5  | 8  | 9  | 10 | 11 |
| 6  | 9  | 10 | 11 | 12 |
| 7  | 10 | 11 | 12 | 13 |
| 8  | 11 | 12 | 13 | 14 |
| 9  | 12 | 13 | 14 | 15 |

1.2.77) Missing blocks filled in...

| +  | 5  | 6  | 7  | 8  | 9  |
| -- | -- | -- | -- | -- | -- |
| 5  | 10 | 11 | 12 | 13 | 14 |
| 6  | 11 | 12 | 13 | 14 | 15 |
| 7  | 12 | 13 | 14 | 15 | 16 |
| 8  | 13 | 14 | 15 | 15 | 16 |
| 9  | 14 | 15 | 16 | 17 | 18 |

1.2.78) Missing blocks filled in...

| +  | 6  | 7  | 8  | 9  |
| -- | -- | -- | -- | -- |
| 6  | 12 | 13 | 14 | 15 |
| 7  | 13 | 14 | 15 | 16 |
| 8  | 14 | 15 | 15 | 16 |
| 9  | 15 | 16 | 17 | 18 |

1.2.79)

a) 0+13=13
b) 13+0=0

1.2.80)

a) 0+5280 = 0
b) 5280+0 = 0

1.2.81)

a) 8+3=11
b) 3+8=11

1.2.82)

a) 7+5=12
b) 5+7=12

1.2.83)

```
   <-- carry over
45
33 +
--
78
```

1.2.84)

```
   <-- carry over
37
22 +
--
59
```

1.2.85)

```
   <-- carry over
71
28 +
--
99
```

1.2.86)

```
   <-- carry over
43
53 +
--
96
```

1.2.87)

```
1  <-- carry over
26
59 +
--
85
```

1.2.88)

```
1  <-- carry over
38
17 +
--
55
```

1.2.89)

```
 1  <-- carry over
 64
 78 +
 --
143
```

1.2.90)

```
 1  <-- carry over
 92
 39 +
 --
131
```

1.2.91)

```
  1  <-- carry over
 168
 325 +
 ---
 493
```

1.2.92)

```
  1  <-- carry over
 247
 149 +
 ---
 396
```

1.2.93)

```
 11  <-- carry over
 584
 277 +
 ---
 861
```

1.2.94)

```
 11  <-- carry over
 175
 648 +
 ---
 823
```

1.2.95)

```
 11  <-- carry over
 832
 199 +
 ---
1031
```

1.2.96)

```
 11  <-- carry over
 775
 369 +
 ---
1144
```

1.2.97)

```
  11  <-- carry over
 6358
  492 +
 ----
 6850
```

1.2.98)

```
  11  <-- carry over
 9184
  578 +
 ----
 9762
```

1.2.99)

```
 111   <-- carry over
  3740
 18593 +
 -----
 22333
```

1.2.100)

```
 111   <-- carry over
  6118
 15990 +
 -----
 22108
```

1.2.101)

```
 11  1  <-- carry over
 485012
 619848 +
 ------
1104860
```

1.2.102)

```
 11111  <-- carry over
 368911
 857289 +
 ------
1226200
```

1.2.103)

```
  211  <-- carry over
 24731
   592
  3868 +
 -----
 29191
```

1.2.104)

```
 1211  <-- carry over
 28925
   817
  4593 +
 -----
 34335
```

1.2.105)

```
 2111  <-- carry over
  8015
 76946
 16570 +
 -----
101531
```

1.2.106)

```
 1111  <-- carry over
  6291
 54107
 28635 +
 -----
 89033
```

1.2.107) 13+18=31

1.2.108) 12+19=31

1.2.109) 90+65=155

1.2.110) 70+38=108

1.2.111) 33+49=82

1.2.112) 68+25=93

1.2.113) 250+599=849

1.2.114) 115+286=401

1.2.115) 628+77=705

1.2.116) 593+79=672

1.2.117) 1482+915=2397

1.2.118) 2719+682=3401

1.2.119) 1100+250+525=1875

1.2.120) 299+35+68=402

1.2.121) 14+19+12+25+68=137

1.2.122) 19+12+23+29+44=115

1.2.123) 238+120+156+196+100+132+225=167

1.2.124)

```
 33  <-- carry over
 175
 192
 148
 169
 205
 181
 225 +
 ---
1295
```

1.2.125)

```
 1111   <-- carry over
 82572
 79316
 75298 +
 -----
237186
```

1.2.126)

```
 11221 <-- carry over
 292540
 505875
 423699 +
 ------
1222114
```

1.2.127) 14+12+18=44

1.2.128) 12+13+5=30

1.2.129) 7+7+21+21=14+42=56

1.2.130) 14+14+19+19=28+38=66

1.2.131) 18+18+19+16=36+35=71

1.2.132) 17+17+24+29=34+24+29=58+29=87

1.2.133) 4+5+3+19+7+24=62

1.2.134) 25+11+7+14+10=67

1.2.135) 320+170+150=640

1.1.136) 420+230+580=1230

1.1.137) 82+91+75+88+70=406 -- yes, it passed

1.1.138) 210+145+183+230+159+164=355+183+230+159+164=585+183+159+164=768+159+164=927+164=1091 -- yes, its below

1.1.139) Very confident

1.1.140) Will codify model as software and embed into notes.

## Chapter 1 Section 1.3

__TRY IT__

1.51)

a) twelve minus four
b) twenty nine minus eleven

1.52)

a) eleven minus two
b) twenty nine minus twelve

1.53) model 9 - 6

```
□□□□□□□□□ 9

    ┌────────┐
□□□ │ □□□□□□ │   remove 6 from 9
 3  └────────┘
        6
```

1.54) model 6 - 1

```
□□□□□□ 6

      ┌───┐
□□□□□ │ □ │ remove 1 from 6
  5   └───┘
        1
```

1.55) model 12 - 7

```
□□□□□□□□□□□□ 12

      ┌─────────┐
□□□□□ │ □□□□□□□ │ remove 7 from 12
  5   └─────────┘
           7
```

1.56) model 14 - 8

```
□□□□□□□□□□□□□□ 14

       ┌──────────┐
□□□□□□ │ □□□□□□□□ │ remove 8 from 14
   6   └──────────┘
           8
```

1.57) model 42 - 27

```
□□□□□□□□□□ 42
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□

□□□□□□□□□□ 15
□□□□□ ┌───────┐
 ┌────┘ □□□□□ │
 │ □□□□□□□□□□ │ 27
 │ □□□□□□□□□□ │
 │ □□ ┌───────┘
 └────┘
```

1.58) model 45 - 29

```
□□□□□□□□□□ 45
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□

□□□□□□□□□□ 16
□□□□□□ ┌──────┐
 ┌─────┘ □□□□ │
 │ □□□□□□□□□□ │ 29
 │ □□□□□□□□□□ │
 │ □□□□□ ┌────┘
 └───────┘
```

1.59) 7-0=7, 7+0=7

1.60) 6-2=4, 4+2=6

1.61) subtract and check: 86-54

`{kt}
\begin{alignedat}{3}
       {}&   \enspace        {}& \\
       {8}&  \enspace        {6}&  \\
       {5}&  \enspace        {4}&  \enspace - \\
\hline
       {3}&  \enspace        {2}&     
\end{alignedat}
`

```
  54
  32 +
  --
  86
```

1.62) subtract and check: 99-74

`{kt}
\begin{alignedat}{3}
       {}&   \enspace        {}& \\
       {9}&  \enspace        {9}&  \\
       {7}&  \enspace        {4}&  \enspace - \\
\hline
       {2}&  \enspace        {5}&     
\end{alignedat}
`

```
  74
  25+
  --
  99
```

1.63) subtract and check: 93-58

`{kt}
\begin{alignedat}{3}
       {8}&  \enspace        {13}& \\
\cancel{9}&  \enspace \cancel{3}&  \\
       {5}&  \enspace        {8}&  \enspace - \\
\hline
       {3}&  \enspace        {5}&     
\end{alignedat}
`

```
  1  <-- carry over
  58
  35 +
  --
  93
```

1.64) subtract and check: 81-39

`{kt}
\begin{alignedat}{3}
       {7}&  \enspace        {11}& \\
\cancel{8}&  \enspace \cancel{1}&  \\
       {3}&  \enspace        {9}&  \enspace - \\
\hline
       {4}&  \enspace        {2}&     
\end{alignedat}
`

```
  1  <-- carry over
  39
  42 +
  --
  81
```

1.65) subtract and check: 439-52

`{kt}
\begin{alignedat}{3}
       {3}&  \enspace        {13}& \enspace        {}&  \\
\cancel{4}&  \enspace \cancel{3}&  \enspace        {9}& \\
        {}&  \enspace        {5}&  \enspace        {2}& \enspace - \\
\hline
       {3}&  \enspace        {8}&  \enspace        {7}&     
\end{alignedat}
`

```
  1   <-- carry over
   52
  387 +
  ---
  439
```

1.66) subtract and check: 318 - 75

`{kt}
\begin{alignedat}{3}
       {2}&  \enspace        {11}& \enspace        {}& \\
\cancel{3}&  \enspace \cancel{1}&  \enspace        {8}& \\
       {}&   \enspace        {7}&  \enspace        {5}& \enspace - \\
\hline
       {2}&  \enspace        {4}&  \enspace        {3}&     
\end{alignedat}
`

```
  1   <-- carry over
  243
   75 +
  ---
  318
```

1.67) subtract and check: 832 - 376

`{kt}
\begin{alignedat}{3}
       {7}&  \enspace        {12}& \enspace        {}& \\
       {}&   \enspace \cancel{2}&  \enspace        {12}& \\
\cancel{8}&  \enspace \cancel{3}&  \enspace \cancel{2}& \\
       {3}&  \enspace        {7}&  \enspace        {6}& \enspace - \\
\hline
       {4}&  \enspace        {5}&  \enspace        {6}&     
\end{alignedat}
`

```
  11  <-- carry over
  376
  456 +
  ---
  832
```

1.68) subtract and check: 847 - 578

`{kt}
\begin{alignedat}{3}
        {7}&  \enspace        {13}& \enspace        {}& \\
        {}&  \enspace \cancel{3}&  \enspace        {17}& \\
\cancel{8}&  \enspace \cancel{4}&  \enspace \cancel{7}& \\
       {5}&  \enspace        {7}&  \enspace        {8}& \enspace - \\
\hline
       {2}&  \enspace        {6}&  \enspace        {9}&     
\end{alignedat}
`

```
  11  <-- carry over
  578
  269 +
  ---
  847
```

1.69) subtract and check: 4585 - 697

`{kt}
\begin{alignedat}{3}
       {}&   \enspace        {14}& \enspace        {17}& \enspace        {}& \\
       {3}&  \enspace \cancel{4}&  \enspace \cancel{7}&  \enspace        {15}& \\
\cancel{4}&  \enspace \cancel{5}&  \enspace \cancel{8}&  \enspace \cancel{5}& \\
       {}&   \enspace        {6}&  \enspace        {9}&  \enspace        {7}& \enspace - \\
\hline
       {3}&  \enspace        {8}&  \enspace        {8}&  \enspace        {8}&     
\end{alignedat}
`

```
 111  <-- carry over
  697
 3888 +
 ----
 4585
```

1.70) subtract and check: 5637 - 899

`{kt}
\begin{alignedat}{3}
       {}&   \enspace        {15}& \enspace        {12}& \enspace        {}& \\ 
       {4}&  \enspace \cancel{5}&  \enspace \cancel{2}&  \enspace        {17}& \\
\cancel{5}&  \enspace \cancel{6}&  \enspace \cancel{3}&  \enspace \cancel{7}& \\
       {}&  \enspace         {8}&  \enspace        {9}&  \enspace        {9}& \enspace - \\
\hline
       {4}&  \enspace        {7}&  \enspace        {3}&  \enspace        {8}&     
\end{alignedat}
`

```
  11  <-- carry over
 1899
 4738 +
 ----
 5637
```

1.71)

* a) 14-9=5
* b) 37-21=16

1.72)

* a) 11-6=5
* b) 67-18=49

1.73) 77-58=19

1.74) 90-73=17

1.75) 648-499=149

1.76) 285-149=136

__EXERCISE__

1.3.141) fifteen minus nine

1.3.142) difference of eighteen and sixteen

1.3.143) subtract thirty five from forty two

1.3.144) sixty four less than forty three

1.3.145) six hundred seventy five minus three hundred fifty

1.3.146) difference between seven hundred ninety and five hundred twenty five

1.3.147) model 5 - 2

```
□□□□□ 5

    ┌────┐
□□□ │ □□ │ 5-2
    └────┘
```

1.3.148) model 8 - 4

```
□□□□□□□□ 8

     ┌──────┐
□□□□ │ □□□□ │ 8-4
     └──────┘
```

1.3.149) model 6 - 3

```
□□□□□□ 6

    ┌─────┐
□□□ │ □□□ │ 6-3
    └─────┘
```

1.3.150) model 7 - 5

```
□□□□□□□ 7

   ┌───────┐
□□ │ □□□□□ │ 7-5
   └───────┘
```

1.3.151) model 18 - 5

```
□□□□□□□□□□
□□□□□□□□   18


□□□□□□□□□□
    ┌───────┐
□□□ │ □□□□□ │ 18-5
    └───────┘
```

1.3.152) model 19 - 8

```
□□□□□□□□□□
□□□□□□□□□  19


□□□□□□□□□□
  ┌──────────┐
□ │ □□□□□□□□ │ 19-8
  └──────────┘
```

1.3.153) model 17 - 8

```
□□□□□□□□□□
□□□□□□□    17


□□□□□□□□□ ┌───┐
 ┌────────┘ □ │
 │ □□□□□□□ ┌──┘ 17-8
 └─────────┘
```

1.3.154) model 17 - 9

```
□□□□□□□□□□
□□□□□□□    17


□□□□□□□□ ┌────┐
 ┌───────┘ □□ │
 │ □□□□□□□ ┌──┘ 17-9
 └─────────┘
```

1.3.155) model 35 - 13

```
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□      35


□□□□□□□□□□
□□□□□□□□□□
□□ ┌──────────┐
 ┌─┘ □□□□□□□□ │
 │ □□□□□ ┌────┘ 35-13
 └───────┘
```

1.3.156) model 32 - 11

```
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□         32


□□□□□□□□□□
□□□□□□□□□□
□ ┌───────────┐
┌─┘ □□□□□□□□□ │
│ □ ┌─────────┘ 32-11
└───┘
```

1.3.157) model 61 - 47

```
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□          61

□□□□□□□□□□
□□□□ ┌────────┐
┌────┘ □□□□□□ │
│ □□□□□□□□□□ ┌┘
│ □□□□□□□□□□ │
│ □□□□□□□□□□ │
│ □□□□□□□□□□ │
│ □ ┌────────┘ 64-47
└───┘
```

1.3.158) model 55 - 36

```
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□□□□□□
□□□□□        55

□□□□□□□□□□
□□□□□□□□□ ┌───┐
┌─────────┘ □ │
│ □□□□□□□□□□ ┌┘
│ □□□□□□□□□□ │
│ □□□□□□□□□□ │
│ □□□□□ ┌────┘  55 - 36
└───────┘
```

1.3.159) 9-4=5

1.3.160) 9-3=6

1.3.161) 8-0=8

1.3.162) 2-0=2

1.3.163)

`{kt}
\begin{alignedat}{3}
       {3}&  \enspace        {8}& \\
       {1}&  \enspace        {6}& \enspace - \\
\hline
       {2}&  \enspace        {2}&     
\end{alignedat}
`

1.3.164)

`{kt}
\begin{alignedat}{3}
       {4}&  \enspace        {5}& \\
       {2}&  \enspace        {1}& \enspace - \\
\hline
       {2}&  \enspace        {4}&     
\end{alignedat}
`

1.3.165)

`{kt}
\begin{alignedat}{3}
       {8}&  \enspace        {5}& \\
       {5}&  \enspace        {2}& \enspace - \\
\hline
       {3}&  \enspace        {3}&     
\end{alignedat}
`

1.3.166)

`{kt}
\begin{alignedat}{3}
       {9}&  \enspace        {9}& \\
       {4}&  \enspace        {7}& \enspace - \\
\hline
       {5}&  \enspace        {2}&     
\end{alignedat}
`

1.3.167)

`{kt}
\begin{alignedat}{3}
       {4}&  \enspace        {9}&  \enspace        {3}& \\
       {3}&  \enspace        {7}&  \enspace        {0}& \enspace - \\
\hline
       {1}&  \enspace        {2}&  \enspace        {3}&     
\end{alignedat}
`

1.3.168)

`{kt}
\begin{alignedat}{3}
       {2}&  \enspace        {6}&  \enspace        {8}& \\
       {1}&  \enspace        {0}&  \enspace        {6}& \enspace - \\
\hline
       {1}&  \enspace        {6}&  \enspace        {2}&     
\end{alignedat}
`

1.3.169)

`{kt}
\begin{alignedat}{4}
       { 5}&  \enspace        { 9}&  \enspace        { 4}&  \enspace        { 6}&  \\
       { 4}&  \enspace        { 6}&  \enspace        { 2}&  \enspace        { 5}&  \enspace - \\
\hline
       { 1}&  \enspace        { 3}&  \enspace        { 2}&  \enspace        { 1}& 
\end{alignedat}
`

1.3.170)

`{kt}
\begin{alignedat}{4}
       { 7}&  \enspace        { 7}&  \enspace        { 7}&  \enspace        { 5}&  \\
       { 3}&  \enspace        { 2}&  \enspace        { 5}&  \enspace        { 1}&  \enspace - \\
\hline
       { 4}&  \enspace        { 5}&  \enspace        { 2}&  \enspace        { 4}& 
\end{alignedat}
`

1.3.171)

`{kt}
\begin{alignedat}{3}
       {6}&  \enspace       {15}& \\
\cancel{7}&  \enspace \cancel{5}& \\
       {4}&  \enspace        {7}& \enspace - \\
\hline
       {2}&  \enspace        {8}&     
\end{alignedat}
`

1.3.172)

`{kt}
\begin{alignedat}{3}
       {5}&  \enspace        {13}& \\
\cancel{6}&  \enspace \cancel{3}& \\
       {5}&  \enspace        {9}& \enspace - \\
\hline
       {0}&  \enspace        {4}&     
\end{alignedat}
`

1.3.173)

`{kt}
\begin{alignedat}{3}
       {}&   \enspace        {5}&  \enspace        {11}& \\
       {4}&  \enspace \cancel{6}&  \enspace \cancel{1}& \\
       {2}&  \enspace        {3}&  \enspace        {9}& \enspace - \\
\hline
       {2}&  \enspace        {2}&  \enspace        {2}&     
\end{alignedat}
`

1.3.174)

`{kt}
\begin{alignedat}{3}
       {}&   \enspace        {7}&  \enspace        {16}& \\
       {4}&  \enspace \cancel{8}&  \enspace \cancel{6}& \\
       {2}&  \enspace        {5}&  \enspace        {7}& \enspace - \\
\hline
       {2}&  \enspace        {2}&  \enspace        {9}&     
\end{alignedat}
`

1.3.175)

`{kt}
\begin{alignedat}{3}
       {4}&  \enspace        {11}& \enspace        {}& \\
       { }&  \enspace \cancel{1}&  \enspace        {15}& \\
\cancel{5}&  \enspace \cancel{2}&  \enspace \cancel{5}& \\
       {1}&  \enspace        {7}&  \enspace        {9}& \enspace - \\
\hline
       {3}&  \enspace        {3}&  \enspace        {6}&     
\end{alignedat}
`

1.3.176)

`{kt}
\begin{alignedat}{3}
       {4}&  \enspace        {13}& \enspace        {}& \\
       { }&  \enspace \cancel{3}&  \enspace        {12}& \\
\cancel{5}&  \enspace \cancel{4}&  \enspace \cancel{2}& \\
       {2}&  \enspace        {8}&  \enspace        {8}& \enspace - \\
\hline
       {2}&  \enspace        {5}&  \enspace        {4}&     
\end{alignedat}
`

1.3.177)

`{kt}
\begin{alignedat}{4}
       { 5}&  \enspace        {12}&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace \cancel{ 2}&  \enspace        {10}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 0}&  \enspace        {18}&  \\
\cancel{ 6}&  \enspace \cancel{ 3}&  \enspace \cancel{ 1}&  \enspace \cancel{ 8}&  \\
       { 2}&  \enspace        { 7}&  \enspace        { 9}&  \enspace        { 9}&  \enspace - \\
\hline
       { 3}&  \enspace        { 5}&  \enspace        { 1}&  \enspace        { 9}& 
\end{alignedat}
`

1.3.178)

`{kt}
\begin{alignedat}{4}
       { 7}&  \enspace        {10}&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace \cancel{ 0}&  \enspace        {14}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 4}&  \enspace        {13}&  \\
\cancel{ 8}&  \enspace \cancel{ 1}&  \enspace \cancel{ 5}&  \enspace \cancel{ 3}&  \\
       { 3}&  \enspace        { 9}&  \enspace        { 7}&  \enspace        { 8}&  \enspace - \\
\hline
       { 4}&  \enspace        { 1}&  \enspace        { 7}&  \enspace        { 5}& 
\end{alignedat}
`

1.3.179)

`{kt}
\begin{alignedat}{4}
       { 1}&  \enspace        {10}&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace \cancel{ 0}&  \enspace        {14}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 4}&  \enspace        {10}&  \\
\cancel{ 2}&  \enspace \cancel{ 1}&  \enspace \cancel{ 5}&  \enspace \cancel{ 0}&  \\
       {  }&  \enspace        { 9}&  \enspace        { 6}&  \enspace        { 4}&  \enspace - \\
\hline
       { 1}&  \enspace        { 1}&  \enspace        { 8}&  \enspace        { 6}& 
\end{alignedat}
`

1.3.180)

`{kt}
\begin{alignedat}{4}
       { 3}&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {11}&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace \cancel{ 1}&  \enspace        {13}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 3}&  \enspace        {15}&  \\
\cancel{ 4}&  \enspace \cancel{ 2}&  \enspace \cancel{ 4}&  \enspace \cancel{ 5}&  \\
       {  }&  \enspace        { 8}&  \enspace        { 9}&  \enspace        { 9}&  \enspace - \\
\hline
       { 3}&  \enspace        { 3}&  \enspace        {  }&  \enspace        { 6}& 
\end{alignedat}
`

1.3.181)

`{kt}
\begin{alignedat}{5}
       { 3}&  \enspace        {12}&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace \cancel{ 2}&  \enspace        {15}&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 5}&  \enspace        {14}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 4}&  \enspace        {10}&  \\
\cancel{ 4}&  \enspace \cancel{ 3}&  \enspace \cancel{ 6}&  \enspace \cancel{ 5}&  \enspace \cancel{ 0}&  \\
       {  }&  \enspace        { 8}&  \enspace        { 9}&  \enspace        { 8}&  \enspace        { 2}&  \enspace - \\
\hline
       { 3}&  \enspace        { 4}&  \enspace        { 6}&  \enspace        { 6}&  \enspace        { 8}&
\end{alignedat}
`

1.3.182)

`{kt}
\begin{alignedat}{5}
       { 2}&  \enspace        {14}&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace \cancel{ 4}&  \enspace        {10}&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 0}&  \enspace        {15}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 5}&  \enspace        {12}&  \\
\cancel{ 3}&  \enspace \cancel{ 5}&  \enspace \cancel{ 1}&  \enspace \cancel{ 6}&  \enspace \cancel{ 2}&  \\
       {  }&  \enspace        { 7}&  \enspace        { 8}&  \enspace        { 8}&  \enspace        { 5}&  \enspace - \\
\hline
       { 2}&  \enspace        { 7}&  \enspace        { 2}&  \enspace        { 7}&  \enspace        { 7}&
\end{alignedat}
`

1.3.183) 10-3 = 7

1.3.184) 12 - 8 = 4

1.3.185) 15 - 4 = 11

1.3.186) 18 - 7 = 11

1.3.187) 9 - 6 = 4

1.3.188) 9 - 8 = 1

1.3.189) 75 - 28 = 47

1.3.190) 81 - 59 = 22

1.3.191) 45-20=25

1.3.192) 37-24=13

1.3.193) 92-67=25

1.3.194) 75-49=26

1.3.195) 16-12=4

1.3.196) 19-15=4

1.3.197) 61-38=23

1.3.198) 62-47=15

1.3.199) 76-47=29

1.3.200) 91-53=38

1.3.201) 256-184=72

1.3.202) 305-262=43

1.3.203)

```
  1  <-- carry over
 719
 341+
 ---
1060
```

1.3.204)

```
  1  <-- carry over
 647
 528+
 ---
1175
```

1.3.205)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        { 9}&  \enspace        {  }&  \enspace        {  }&  \\
       { 1}&  \enspace \cancel{10}&  \enspace        {11}&  \enspace        {  }&  \\
\cancel{ 2}&  \enspace \cancel{ 0}&  \enspace \cancel{ 1}&  \enspace        { 5}&  \\
       { 1}&  \enspace        { 9}&  \enspace        { 9}&  \enspace        { 3}&  \enspace - \\
\hline
       { 0}&  \enspace        { 0}&  \enspace        { 2}&  \enspace        { 2}& 
\end{alignedat}
`

1.3.206)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        { 9}&  \enspace        {  }&  \enspace        {  }&  \\
       { 1}&  \enspace \cancel{10}&  \enspace        {11}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace        {10}&  \\
\cancel{ 2}&  \enspace \cancel{ 0}&  \enspace \cancel{ 2}&  \enspace \cancel{ 0}&  \\
       { 1}&  \enspace        { 9}&  \enspace        { 8}&  \enspace        { 4}&  \enspace - \\
\hline
       { 0}&  \enspace        { 0}&  \enspace        { 3}&  \enspace        { 6}& 
\end{alignedat}
`

1.3.207) 35+75=110

1.3.208) 33+60=93

1.3.209) 41-13=28

1.3.210) 36-28=8

1.3.211) 100-76=24

1.3.212) 1000-945=55

1.3.213) 80-63=17

1.3.214) 97-73=24

1.3.215) 35-22=13

1.3.216) 82-46=36

1.3.217) 650-399=251

1.3.218) 1600-755=845

1.3.219) 840-685=155

1.3.220) 1125-892=233

1.3.221) 115+230=345 502-345=157

1.3.222) 75+50+70+80=275 350-275=75

1.3.223) one is the opposite of the other

1.3.224) verification

## Chapter 1 Section 1.4

__TRY IT__

1.77)

* a) eight times seven
* b) eighteen times eleven

1.78)

* a) thirteen times seven
* b) five times sixteen

1.79)

```
□□□□
□□□□
□□□□
□□□□
□□□□
□□□□
```

1.80)

```
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
```

1.81)

* a) 0 * 11 = 0
* b) 39 * 0 = 0

1.82)

* a) 0 * 24 = 0
* b) 57 * 0 = 0

1.83)

* a) 19 * 1 = 19
* b) 1 * 39 = 39

1.84)

* a) 24 * 1 = 24
* b) 1 * 57 = 57

1.85)

* a) 9*6=54
* b) 6*9=54

1.86)

* a) 8*6=48
* b) 6*8=48

1.87)

```
 3  <-- carry over
 64
  8 *
 --
512
```

1.88)

```
 4  <-- carry over
 57
  6 *
 --
342
```

1.89)

```
 23  <-- carry over
 347
   5 *
 ---
1705
```

1.90)

```
 41  <-- carry over
 462
   7
 ---
3234   
```

1.91)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 3}&  \\
       {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 8}&  \enspace * \\
\hline
       {  }&  \enspace        { 3}&  \enspace        { 2}&  \enspace        { 4}&  \\
       { 3}&  \enspace        { 0}&  \enspace        { 1}&  \enspace        { 0}&  \enspace + \\
\hline
       { 3}&  \enspace        { 3}&  \enspace        { 3}&  \enspace        { 4}& 
\end{alignedat}
`

1.92)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 3}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace        { 4}&  \\
       {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 9}&  \enspace * \\
\hline
       {  }&  \enspace        { 5}&  \enspace        { 7}&  \enspace        { 6}&  \\
       { 3}&  \enspace        { 2}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
       { 3}&  \enspace        { 7}&  \enspace        { 7}&  \enspace        { 6}& 
\end{alignedat}
`

1.93)

* a) `{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 7}&  \\
       {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 4}&  \enspace        { 7}&  \enspace        { 0}&  \\
\hline
       {  }&  \enspace        { 4}&  \enspace        { 7}&  \enspace        { 0}&
\end{alignedat}
`

* b) `{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 7}&  \\
       {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 0}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
       { 4}&  \enspace        { 7}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
       { 4}&  \enspace        { 7}&  \enspace        { 0}&  \enspace        { 0}&
\end{alignedat}
`

1.94)

* a) `{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 5}&  \\
       {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 7}&  \enspace        { 5}&  \enspace        { 0}&  \\
\hline
       {  }&  \enspace        { 7}&  \enspace        { 5}&  \enspace        { 0}&
\end{alignedat}
`

* b) `{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 5}&  \\
       {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 0}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
       { 7}&  \enspace        { 5}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
       { 7}&  \enspace        { 5}&  \enspace        { 0}&  \enspace        { 0}&
\end{alignedat}
`

1.95)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 4}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 4}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 8}&  \enspace        { 3}&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 6}&  \enspace        { 5}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 4}&  \enspace        { 1}&  \enspace        { 5}&  \\
       {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 8}&  \enspace        { 9}&  \enspace        { 8}&  \enspace        { 0}&  \\
       {  }&  \enspace        {  }&  \enspace        { 9}&  \enspace        { 6}&  \enspace        { 6}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
       {  }&  \enspace        { 1}&  \enspace        { 2}&  \enspace        { 7}&  \enspace        { 9}&  \enspace        { 9}&  \enspace        { 5}& 
\end{alignedat}
`

1.96)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 2}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace \cancel{ 2}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 2}&  \enspace        { 3}&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 9}&  \enspace        { 4}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 2}&  \enspace        { 9}&  \enspace        { 2}&  \\
       {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 4}&  \enspace        { 0}&  \enspace        { 7}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 5}&  \enspace        { 7}&  \enspace        { 6}&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
       {  }&  \enspace        { 6}&  \enspace        { 5}&  \enspace        { 3}&  \enspace        { 4}&  \enspace        { 6}&  \enspace        { 2}& 
\end{alignedat}
`

1.97)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 7}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 1}&  \enspace        { 8}&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 0}&  \enspace        { 9}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace        { 4}&  \enspace        { 6}&  \enspace        { 2}&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 3}&  \enspace        { 5}&  \enspace        { 9}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
       {  }&  \enspace        { 3}&  \enspace        { 6}&  \enspace        { 5}&  \enspace        { 4}&  \enspace        { 6}&  \enspace        { 2}& 
\end{alignedat}
`

1.98)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 5}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 2}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace        { 2}&  \enspace        { 7}&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 0}&  \enspace        { 4}&  \enspace * \\
\hline
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 5}&  \enspace        { 0}&  \enspace        { 8}&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 4}&  \enspace        { 9}&  \enspace        { 1}&  \enspace        { 4}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
       {  }&  \enspace        { 4}&  \enspace        { 9}&  \enspace        { 3}&  \enspace        { 9}&  \enspace        { 0}&  \enspace        { 8}& 
\end{alignedat}
`

1.99)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        { 2}&  \enspace        {  }&  \\
       {  }&  \enspace        { 1}&  \enspace        { 3}&  \\
       {  }&  \enspace        { 2}&  \enspace        { 8}&  \enspace * \\
\hline
       { 1}&  \enspace        { 0}&  \enspace        { 4}&  \\
       { 2}&  \enspace        { 6}&  \enspace        { 0}&  \enspace + \\
\hline
       { 2}&  \enspace        { 6}&  \enspace        { 4}& 
\end{alignedat}
`

1.100)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        { 2}&  \enspace        {  }&  \\
       {  }&  \enspace        { 4}&  \enspace        { 7}&  \\
       {  }&  \enspace        { 1}&  \enspace        { 4}&  \enspace * \\
\hline
       { 1}&  \enspace        { 8}&  \enspace        { 8}&  \\
       { 4}&  \enspace        { 7}&  \enspace        { 0}&  \enspace + \\
\hline
       { 6}&  \enspace        { 5}&  \enspace        { 8}& 
\end{alignedat}
`

1.101)

`{kt}
\begin{alignedat}{4}
       { 1}&  \enspace        { 1}&  \enspace        {  }&  \\
       { 2}&  \enspace        { 5}&  \enspace        { 8}&  \\
       {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace * \\
\hline
       { 5}&  \enspace        { 1}&  \enspace        { 6}&  \\
\end{alignedat}
`

1.102)

`{kt}
\begin{alignedat}{4}
       { 1}&  \enspace        { 1}&  \enspace        {  }&  \\
       { 1}&  \enspace        { 7}&  \enspace        { 7}&  \\
       {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace * \\
\hline
       { 2}&  \enspace        { 5}&  \enspace        { 4}&  \\
\end{alignedat}
`

1.103)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        { 2}&  \enspace        {  }&  \\
       {  }&  \enspace        { 2}&  \enspace        { 4}&  \\
       {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace * \\
\hline
       { 1}&  \enspace        { 4}&  \enspace        { 4}&  \\
\end{alignedat}
`

1.104) 8 * 10 = 80

1.105) 2*14=28

1.106) 2*18=36

1.107) 16*20=320

1.108)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 4}&  \\
       {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 5}&  \enspace * \\
\hline
       {  }&  \enspace        { 1}&  \enspace        { 2}&  \enspace        { 0}&  \\
       {  }&  \enspace        { 9}&  \enspace        { 6}&  \enspace        { 0}&  \enspace + \\
\hline
       { 1}&  \enspace        { 0}&  \enspace        { 8}&  \enspace        { 0}& 
\end{alignedat}
`

1.109) 8 * 50 = 40

1.110) 45 * 20 = 900


__EXERCISE__

1.4.225) product of four and seven

1.4.226) eight times six

1.4.227) product of five and twelve

1.4.228) three times nine

1.4.229) ten times twenty five

1.4.230) twenty times fifteen

1.4.231) forty two times thirty three

1.4.232) thirty nine times sixty four

1.2.233)

```
□□□
□□□
□□□
□□□
□□□
□□□
```

1.2.234)

```
□□□□
□□□□
□□□□
□□□□
□□□□
```


1.2.235)

```
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
□□□□□
```

1.2.237)

| x  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|----|----|----|----|----|----|
| 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |
| 1  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| 2  | 0  | 2  | 4  | 6  | 8  | 10 | 12 | 14 | 16 | 18 |
| 3  | 0  | 3  | 6  | 9  | 12 | 15 | 18 | 21 | 24 | 27 |
| 4  | 0  | 4  | 8  | 12 | 15 | 20 | 24 | 28 | 32 | 36 |
| 5  | 0  | 5  | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 |
| 6  | 0  | 6  | 12 | 18 | 24 | 30 | 36 | 42 | 48 | 54 |
| 7  | 0  | 7  | 14 | 21 | 28 | 35 | 42 | 49 | 56 | 63 |
| 8  | 0  | 8  | 16 | 24 | 32 | 40 | 48 | 56 | 64 | 72 |
| 9  | 0  | 9  | 18 | 27 | 36 | 45 | 54 | 63 | 72 | 81 |

1.2.238)

| x  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|----|----|----|----|----|----|
| 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |
| 1  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| 2  | 0  | 2  | 4  | 6  | 8  | 10 | 12 | 14 | 16 | 18 |
| 3  | 0  | 3  | 6  | 9  | 12 | 15 | 18 | 21 | 24 | 27 |
| 4  | 0  | 4  | 8  | 12 | 16 | 20 | 24 | 28 | 32 | 36 |
| 5  | 0  | 5  | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 |
| 6  | 0  | 6  | 12 | 18 | 24 | 30 | 36 | 42 | 48 | 54 |
| 7  | 0  | 7  | 14 | 21 | 28 | 35 | 42 | 49 | 56 | 63 |
| 8  | 0  | 8  | 16 | 24 | 32 | 40 | 48 | 56 | 64 | 72 |
| 9  | 0  | 9  | 18 | 27 | 36 | 45 | 56 | 63 | 72 | 81 |


1.2.239)

| x  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|----|----|----|
| 4  | 12 | 16 | 20 | 24 | 28 | 32 | 36 |
| 5  | 15 | 20 | 25 | 30 | 35 | 40 | 45 |
| 6  | 18 | 24 | 30 | 36 | 42 | 48 | 54 |
| 7  | 21 | 28 | 35 | 42 | 49 | 56 | 63 |
| 8  | 24 | 32 | 40 | 48 | 56 | 64 | 72 |
| 9  | 27 | 36 | 45 | 54 | 63 | 72 | 81 |

1.2.240)

| x  | 4  | 5  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|----|----|
| 3  | 12 | 15 | 18 | 21 | 24 | 27 |
| 4  | 16 | 20 | 24 | 28 | 32 | 36 |
| 5  | 20 | 25 | 30 | 35 | 40 | 45 |
| 6  | 24 | 30 | 36 | 42 | 48 | 54 |
| 7  | 28 | 35 | 42 | 49 | 56 | 63 |
| 8  | 32 | 40 | 48 | 56 | 64 | 72 |
| 9  | 36 | 45 | 54 | 63 | 72 | 81 |

1.2.241)

| x  | 4  | 5  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|----|----|
| 6  | 24 | 30 | 36 | 42 | 48 | 54 |
| 7  | 28 | 35 | 42 | 49 | 56 | 63 |
| 8  | 32 | 40 | 48 | 56 | 64 | 72 |
| 9  | 36 | 45 | 54 | 63 | 72 | 91 |

1.2.242)

| x  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|
| 3  | 18 | 21 | 24 | 27 |
| 4  | 24 | 28 | 32 | 36 |
| 5  | 30 | 35 | 40 | 45 |
| 6  | 36 | 42 | 48 | 54 |
| 7  | 42 | 49 | 56 | 63 |
| 8  | 68 | 56 | 64 | 72 |
| 9  | 54 | 63 | 72 | 81 |

1.2.243)

| x  | 5  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|----|
| 5  | 25 | 30 | 35 | 40 | 45 |
| 6  | 30 | 36 | 42 | 48 | 54 |
| 7  | 35 | 42 | 49 | 56 | 63 |
| 8  | 40 | 48 | 56 | 64 | 72 |
| 9  | 45 | 54 | 63 | 72 | 91 |

1.2.244)

| x  | 6  | 7  | 8  | 9  |
|----|----|----|----|----|
| 6  | 36 | 42 | 48 | 54 |
| 7  | 42 | 49 | 56 | 63 |
| 8  | 48 | 56 | 64 | 72 |
| 9  | 54 | 63 | 72 | 91 |

1.2.245) 0 * 15 = 15

1.2.246) 0 * 41 = 0

1.2.247) 99 * 0 = 0

1.2.248) 77 * 0 = 0

1.2.249) 1 * 43 = 43

1.2.250) 1 * 34 = 34

1.2.251) 28 * 1 = 1

1.2.252) 65 * 1 = 1

1.2.253) 1 * 240055 = 240055

1.2.254) 1 * 189206 = 189206

1.2.255) 

* a) 7*6 = 42
* b) 6*7 = 42

1.2.256)

* a) 8 * 9 = 72
* b) 9 * 8 = 72

1.2.257)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        { 4}&  \enspace        {  }&  \\
       {  }&  \enspace        { 7}&  \enspace        { 9}&  \\
       {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace * \\
\hline
       { 3}&  \enspace        { 9}&  \enspace        { 5}&
\end{alignedat}
`

1.2.258)

`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        { 3}&  \enspace        {  }&  \\
       {  }&  \enspace        { 5}&  \enspace        { 8}&  \\
       {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace * \\
\hline
       { 2}&  \enspace        { 3}&  \enspace        { 2}&
\end{alignedat}
`

1.2.259)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        { 4}&  \enspace        { 3}&  \enspace        {  }&  \\
        {  }&  \enspace        { 2}&  \enspace        { 7}&  \enspace        { 5}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace * \\
\hline
        { 1}&  \enspace        { 6}&  \enspace        { 5}&  \enspace        { 0}&
\end{alignedat}
`

1.2.260)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        { 1}&  \enspace        { 4}&  \enspace        {  }&  \\
        {  }&  \enspace        { 6}&  \enspace        { 3}&  \enspace        { 8}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace * \\
\hline
        { 3}&  \enspace        { 1}&  \enspace        { 9}&  \enspace        { 0}&
\end{alignedat}
`

1.2.261)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        { 2}&  \enspace        { 1}&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        { 3}&  \enspace        { 4}&  \enspace        { 2}&  \enspace        { 1}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace * \\
\hline
        { 2}&  \enspace        { 3}&  \enspace        { 9}&  \enspace        { 4}&  \enspace        { 7}&
\end{alignedat}
`

1.2.262)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        { 9}&  \enspace        { 1}&  \enspace        { 4}&  \enspace        { 3}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace * \\
\hline
        { 2}&  \enspace        { 7}&  \enspace        { 4}&  \enspace        { 2}&  \enspace        { 9}&
\end{alignedat}
`

1.2.263)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 2}&  \\
        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 8}&  \enspace * \\
\hline
        {  }&  \enspace        { 4}&  \enspace        { 1}&  \enspace        { 6}&  \\
        { 1}&  \enspace        { 5}&  \enspace        { 6}&  \enspace        { 0}&  \enspace + \\
\hline
        { 1}&  \enspace        { 9}&  \enspace        { 7}&  \enspace        { 6}& 
\end{alignedat}
`

1.2.264)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 3}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 7}&  \\
        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 5}&  \enspace * \\
\hline
        {  }&  \enspace        { 1}&  \enspace        { 8}&  \enspace        { 5}&  \\
        { 1}&  \enspace        { 4}&  \enspace        { 8}&  \enspace        { 0}&  \enspace + \\
\hline
        { 1}&  \enspace        { 6}&  \enspace        { 6}&  \enspace        { 5}& 
\end{alignedat}
`

1.2.265)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 9}&  \enspace        { 6}&  \\
        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 3}&  \enspace * \\
\hline
        {  }&  \enspace        { 2}&  \enspace        { 8}&  \enspace        { 8}&  \\
        { 6}&  \enspace        { 7}&  \enspace        { 2}&  \enspace        { 0}&  \enspace + \\
\hline
        { 7}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 8}& 
\end{alignedat}
`

1.2.266)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 5}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 9}&  \\
        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 6}&  \enspace * \\
\hline
        {  }&  \enspace        { 4}&  \enspace        { 8}&  \enspace        { 4}&  \\
        { 4}&  \enspace        { 4}&  \enspace        { 5}&  \enspace        { 0}&  \enspace + \\
\hline
        { 4}&  \enspace        { 9}&  \enspace        { 3}&  \enspace        { 4}& 
\end{alignedat}
`

1.2.267)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 3}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 7}&  \\
        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 5}&  \enspace * \\
\hline
        {  }&  \enspace        { 1}&  \enspace        { 3}&  \enspace        { 5}&  \\
        { 2}&  \enspace        { 1}&  \enspace        { 6}&  \enspace        { 0}&  \enspace + \\
\hline
        { 2}&  \enspace        { 2}&  \enspace        { 9}&  \enspace        { 5}& 
\end{alignedat}
`

1.2.268)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 3}&  \\
        {  }&  \enspace        {  }&  \enspace        { 9}&  \enspace        { 8}&  \enspace * \\
\hline
        {  }&  \enspace        { 4}&  \enspace        { 2}&  \enspace        { 4}&  \\
        { 4}&  \enspace        { 7}&  \enspace        { 7}&  \enspace        { 0}&  \enspace + \\
\hline
        { 5}&  \enspace        { 1}&  \enspace        { 9}&  \enspace        { 4}& 
\end{alignedat}
`

1.2.269) 23 * 10 = 230

1.2.270) 19 * 10 = 190

1.2.271) 100 * 36 = 3600

1.2.272) 100 * 25 = 2500

1.2.273) 1000 * 88 = 88000

1.2.274) 1000 * 46 = 46000

1.2.275) 50 * 1000000 = 50000000

1.2.276) 30 * 1000000 = 30000000

1.2.277)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 6}&  \enspace \cancel{ 6}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 4}&  \enspace        { 7}&  \\
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 3}&  \enspace        { 9}&  \enspace * \\
\hline
        {  }&  \enspace        { 2}&  \enspace        { 4}&  \enspace        { 2}&  \enspace        { 3}&  \\
        {  }&  \enspace        { 7}&  \enspace        { 4}&  \enspace        { 1}&  \enspace        { 0}&  \\
        { 2}&  \enspace        { 4}&  \enspace        { 7}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 3}&  \enspace        { 4}&  \enspace        { 5}&  \enspace        { 3}&  \enspace        { 3}& 
\end{alignedat}
`

1.2.278)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 4}&  \enspace \cancel{ 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 5}&  \enspace        { 6}&  \\
        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 2}&  \enspace        { 8}&  \enspace * \\
\hline
        {  }&  \enspace        { 1}&  \enspace        { 2}&  \enspace        { 4}&  \enspace        { 8}&  \\
        {  }&  \enspace        { 3}&  \enspace        { 1}&  \enspace        { 2}&  \enspace        { 0}&  \\
        { 4}&  \enspace        { 6}&  \enspace        { 8}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 5}&  \enspace        { 1}&  \enspace        { 1}&  \enspace        { 6}&  \enspace        { 8}& 
\end{alignedat}
`

1.2.279)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace        { 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 8}&  \enspace        { 6}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 2}&  \enspace        { 1}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 8}&  \enspace        { 6}&  \\
        {  }&  \enspace        { 1}&  \enspace        { 1}&  \enspace        { 7}&  \enspace        { 2}&  \enspace        { 0}&  \\
        { 4}&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 2}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 4}&  \enspace        { 2}&  \enspace        { 2}&  \enspace        { 5}&  \enspace        { 0}&  \enspace        { 6}& 
\end{alignedat}
`

1.2.280)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 3}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 3}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 7}&  \enspace        { 2}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 5}&  \enspace        { 5}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 3}&  \enspace        { 6}&  \enspace        { 0}&  \\
        {  }&  \enspace        { 2}&  \enspace        { 3}&  \enspace        { 6}&  \enspace        { 0}&  \enspace        { 0}&  \\
        { 3}&  \enspace        { 2}&  \enspace        { 7}&  \enspace        { 6}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 3}&  \enspace        { 5}&  \enspace        { 3}&  \enspace        { 5}&  \enspace        { 6}&  \enspace        { 0}& 
\end{alignedat}
`

1.2.281)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace \cancel{ 3}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 9}&  \enspace        { 1}&  \enspace        { 5}&  \\
        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 7}&  \enspace        { 9}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 2}&  \enspace        { 3}&  \enspace        { 5}&  \\
        {  }&  \enspace        { 6}&  \enspace        { 4}&  \enspace        { 0}&  \enspace        { 5}&  \enspace        { 0}&  \\
        { 7}&  \enspace        { 3}&  \enspace        { 2}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 8}&  \enspace        { 0}&  \enspace        { 4}&  \enspace        { 2}&  \enspace        { 8}&  \enspace        { 5}& 
\end{alignedat}
`

1.2.282)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace        { 7}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 4}&  \enspace \cancel{ 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 9}&  \enspace        { 6}&  \enspace        { 8}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 9}&  \enspace        { 2}&  \enspace        { 6}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 8}&  \enspace        { 0}&  \enspace        { 8}&  \\
        {  }&  \enspace        { 1}&  \enspace        { 9}&  \enspace        { 3}&  \enspace        { 6}&  \enspace        { 0}&  \\
        { 8}&  \enspace        { 7}&  \enspace        { 1}&  \enspace        { 2}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 8}&  \enspace        { 9}&  \enspace        { 6}&  \enspace        { 3}&  \enspace        { 6}&  \enspace        { 8}& 
\end{alignedat}
`

1.2.283)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 5}&  \enspace        { 6}&  \\
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 4}&  \enspace * \\
\hline
        {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 2}&  \enspace        { 4}&  \\
        {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
        { 2}&  \enspace        { 5}&  \enspace        { 6}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 2}&  \enspace        { 6}&  \enspace        { 6}&  \enspace        { 2}&  \enspace        { 4}& 
\end{alignedat}
`

1.2.284)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 9}&  \enspace        { 7}&  \\
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 3}&  \enspace * \\
\hline
        {  }&  \enspace        { 1}&  \enspace        { 4}&  \enspace        { 9}&  \enspace        { 1}&  \\
        {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
        { 4}&  \enspace        { 9}&  \enspace        { 7}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 5}&  \enspace        { 1}&  \enspace        { 1}&  \enspace        { 9}&  \enspace        { 1}& 
\end{alignedat}
`

1.2.285)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 5}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace \cancel{ 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 4}&  \enspace        { 8}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 0}&  \enspace        { 5}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 7}&  \enspace        { 4}&  \enspace        { 0}&  \\
        {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
        { 2}&  \enspace        { 4}&  \enspace        { 3}&  \enspace        { 6}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 2}&  \enspace        { 4}&  \enspace        { 5}&  \enspace        { 3}&  \enspace        { 4}&  \enspace        { 0}& 
\end{alignedat}
`

1.2.286)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 3}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 8}&  \enspace        { 5}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 6}&  \enspace        { 0}&  \enspace        { 2}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 9}&  \enspace        { 7}&  \enspace        { 0}&  \\
        {  }&  \enspace        {  }&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \\
        { 2}&  \enspace        { 4}&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 2}&  \enspace        { 4}&  \enspace        { 1}&  \enspace        { 9}&  \enspace        { 7}&  \enspace        { 0}& 
\end{alignedat}
`

1.2.287)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        {  }&  \enspace        { 4}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace        {  }&  \enspace \cancel{ 3}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 7}&  \enspace        { 1}&  \enspace        { 9}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 4}&  \enspace        { 3}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 1}&  \enspace        { 5}&  \enspace        { 7}&  \\
        {  }&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 8}&  \enspace        { 7}&  \enspace        { 6}&  \enspace        { 0}&  \\
        { 1}&  \enspace        { 3}&  \enspace        { 5}&  \enspace        { 9}&  \enspace        { 5}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        {  1}&  \enspace        { 4}&  \enspace        { 7}&  \enspace        { 6}&  \enspace        { 3}&  \enspace        { 1}&  \enspace        { 7}& 
\end{alignedat}
`

1.2.288)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 4}&  \enspace        { 5}&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 1}&  \enspace \cancel{ 1}&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace \cancel{ 3}&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 5}&  \enspace        { 8}&  \enspace        { 1}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 2}&  \enspace        { 4}&  \enspace * \\
\hline
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        { 4}&  \enspace        { 3}&  \enspace        { 2}&  \enspace        { 4}&  \\
        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 1}&  \enspace        { 6}&  \enspace        { 2}&  \enspace        { 0}&  \\
        { 2}&  \enspace        { 5}&  \enspace        { 0}&  \enspace        { 6}&  \enspace        { 7}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 2}&  \enspace        { 5}&  \enspace        { 9}&  \enspace        { 2}&  \enspace        { 6}&  \enspace        { 4}&  \enspace        { 4}& 
\end{alignedat}
`

1.2.289) 18 * 33 = 540 + 54 = 594

1.2.290) 15 * 22 = 300 + 30 = 330

1.2.291) 51 * 67 = 3060 + 357 = 3417

1.2.292) 48 * 71 = 3360 + 48 = 3408

1.2.293) 2 * 249 = 498

1.2.294) 2 * 589 = 1178

1.2.295) 10 * 375 = 3750

1.2.296) 10 * 255 = 2550

1.2.297)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 5}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 8}&  \\
        {  }&  \enspace        {  }&  \enspace        { 3}&  \enspace        { 7}&  \enspace * \\
\hline
        {  }&  \enspace        { 2}&  \enspace        { 6}&  \enspace        { 6}&  \\
        { 1}&  \enspace        { 1}&  \enspace        { 4}&  \enspace        { 0}&  \enspace + \\
\hline
        { 1}&  \enspace        { 4}&  \enspace        { 0}&  \enspace        { 6}& 
\end{alignedat}
`

1.2.298)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        { 1}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace \cancel{ 5}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 8}&  \enspace        { 6}&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 9}&  \enspace * \\
\hline
        {  }&  \enspace        { 7}&  \enspace        { 7}&  \enspace        { 4}&  \\
        { 1}&  \enspace        { 7}&  \enspace        { 2}&  \enspace        { 0}&  \enspace + \\
\hline
        { 2}&  \enspace        { 4}&  \enspace        { 9}&  \enspace        { 4}& 
\end{alignedat}
`

1.2.299)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {10}&  \enspace        {  }&  \\
        { 3}&  \enspace \cancel{ 0}&  \enspace        {15}&  \\
 \cancel{ 4}&  \enspace \cancel{ 1}&  \enspace \cancel{ 5}&  \\
        { 2}&  \enspace        { 6}&  \enspace        { 7}&  \enspace - \\
\hline
        { 1}&  \enspace        { 4}&  \enspace        { 8}&  
\end{alignedat}
`

1.2.300)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {13}&  \enspace        {  }&  \\
        { 2}&  \enspace \cancel{ 3}&  \enspace        {11}&  \\
 \cancel{ 3}&  \enspace \cancel{ 4}&  \enspace \cancel{ 1}&  \\
        { 2}&  \enspace        { 8}&  \enspace        { 5}&  \enspace - \\
\hline
        { 0}&  \enspace        { 5}&  \enspace        { 6}&  
\end{alignedat}
`

1.2.301)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        { 1}&  \enspace        { 1}&  \enspace        { 1}&  \enspace        {  }&  \\
        {  }&  \enspace        { 6}&  \enspace        { 2}&  \enspace        { 5}&  \enspace        { 1}&  \\
        {  }&  \enspace        { 4}&  \enspace        { 7}&  \enspace        { 4}&  \enspace        { 9}&  \enspace + \\
\hline
        { 1}&  \enspace        { 1}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}& 
\end{alignedat}
`

1.2.302)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        { 1}&  \enspace        { 1}&  \enspace        { 1}&  \enspace        {  }&  \\
        {  }&  \enspace        { 3}&  \enspace        { 8}&  \enspace        { 1}&  \enspace        { 6}&  \\
        {  }&  \enspace        { 8}&  \enspace        { 1}&  \enspace        { 8}&  \enspace        { 4}&  \enspace + \\
\hline
        { 1}&  \enspace        { 2}&  \enspace        { 0}&  \enspace        { 0}&  \enspace        { 0}& 
\end{alignedat}
`


1.2.303)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace \cancel{ 2}&  \enspace        {  }&  \\
        {  }&  \enspace        {  }&  \enspace        { 2}&  \enspace        { 0}&  \enspace        { 4}&  \\
        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        { 5}&  \enspace        { 6}&  \enspace * \\
\hline
        {  }&  \enspace        { 1}&  \enspace        { 2}&  \enspace        { 2}&  \enspace        { 4}&  \\
        { 1}&  \enspace        { 0}&  \enspace        { 2}&  \enspace        { 0}&  \enspace        { 0}&  \enspace + \\
\hline
        { 1}&  \enspace        { 1}&  \enspace        { 4}&  \enspace        { 2}&  \enspace        { 4}& 
\end{alignedat}
`

1.2.304)

`{kt}
\begin{alignedat}{4}
        {  }&  \enspace        { 8}&  \enspace        { 0}&  \enspace        { 1}&  \\
        {  }&  \enspace        {  }&  \enspace        { 7}&  \enspace        { 7}&  \enspace * \\
\hline
        {  }&  \enspace        { 8}&  \enspace        { 0}&  \enspace        { 7}&  \\
        { 8}&  \enspace        { 0}&  \enspace        { 7}&  \enspace        { 0}&  \enspace + \\
\hline
        { 8}&  \enspace        { 8}&  \enspace        { 7}&  \enspace        { 7}& 
\end{alignedat}
`

1.2.305) 947 * 0 = 0

1.2.306) 947 + 0 = 947

1.2.307) 15382 + 1 = 15383

1.2.308) 15382 * 1 = 15383

1.2.309) 50 - 18 = 32

1.2.310) 90 - 66 = 24

1.2.311) 2 * 35 = 70

1.2.312) 2 * 140 = 280

1.2.313) 2 * 980 = 1800 + 160 + 0 = 1960

1.2.314) 325 + 65 = 390

1.2.315) 875 * 12 = 8750 + 1750 = 10500 

1.2.316) 905 * 15 = 9050 + 4525 = 13575

1.2.317) 89 - 74 = 15

1.2.318) 99 - 45 = 54

1.2.319) 3075 + 950 = 4025

1.2.320) 6308 + 724 = 7032

1.2.321) 814 - 366 = 448

1.2.322) 925 - 388 = 537

1.2.323) 9 * 6 = 54

1.2.324) 6 * 4 = 24

1.2.325) 7 * 44 = 308

1.2.326) 24 * 8 = 192

1.2.327) 15 * 12 = 150 + 30 = 180

1.2.328) 28 * 26 = 560 + 168 = 728

1.2.329) 2 * 10 = 20

1.2.330) 12 * 2 = 24

1.2.331) 50 * 2 = 100

1.2.332) 30 * 2 = 60

1.2.333) 13 * 9 = 117

1.2.334) 18 * 3 = 54

1.2.335) 42 * 34 = 1428

1.2.336) 23 * 28 = 644

1.2.337) 94 * 50 = 4700

1.2.338) 360 * 160 = 36660

1.2.339) 300 * 12 = 3600

1.2.340) 200 * 24 = 4800

1.2.341) yes 

1.2.342) verification

## Chapter 1 Section 1.5

__TRY IT__

1.111)

* a) eighty four divided by seven
* b) eighteen divided by six
* c) twenty four divided by eighty

1.112)

* a) seventy two divided by nine
* b) twenty one divided by three
* c) fifty four divided by six

1.113)

```
□□□□□□ □□□□□□ □□□□□□ □□□□□□
   6      6      6      6
24 total
```

1.114)

```
□□□□□□□ □□□□□□□ □□□□□□□ □□□□□□□ □□□□□□□ □□□□□□□
   7       7       7       7       7       7
42 total
```

1.115)

* a) 54 / 6 = 9, 6 * 9 = 54
* b) 27 / 9 = 3, 3 * 9 = 27

1.116)

* a) 36/9=4, 9*4=36
* b) 40/8=5, 8*5=40

1.117)

* a) 14/14=1, 14*14=14
* b) 27/1=27, 1*27=27

1.118)

* a) 16/1=16, 16*1=16
* b) 4/1=4, 4*1=4

1.119)

* a) 0/2=0, 0*2=0
* b) 17/0=undefined, ?*0=0 (anything multipled by 0 is always 0, it will never result in 17)

1.120)

* a) 0/6=0, 0*6=0
* b) 13/0=undefined, ?*0=0 (anything multipled by 0 is always 0, it will never result in 17)

1.121)

```{ktlongdiv}
   {0659}
{4}{2636}
   {0}
   {\underline{2}}
   {26}
   {\underline{24}}
   {023}
   {\underline{020}}
   {0036}
   {\underline{0036}}
   {0000}
```

```{ktvertmul}
{ }{2}{3}{ }
{ }{6}{5}{9}
{ }{ }{ }{4}
------------
{2}{6}{3}{6}
```

1.122)

```{ktlongdiv}
   {0679}
{4}{2716}
   {0}
   {\underline{2}}
   {27}
   {\underline{24}}
   {031}
   {\underline{028}}
   {0036}
   {\underline{0036}}
   {0000}
```

```{ktvertmul}
{ }{3}{3}{ }
{ }{6}{7}{9}
{ }{ }{ }{4}
------------
{2}{7}{1}{6}
```

1.123)

```{ktlongdiv}
   {0861}
{5}{4305}
   {0}
   {\underline{43}}
   {40}
   {030}
   {\underline{030}}
   {0005}
```

```{ktvertmul}
{ }{3}{ }{ }
{ }{8}{6}{1}
{ }{ }{ }{5}
------------
{4}{3}{0}{5}
```

1.124)

```{ktlongdiv}
   {0651}
{6}{3906}
   {0}
   {\underline{39}}
   {36}
   {030}
   {\underline{030}}
   {0006}
   {\underline{0006}}
   {0000}
```

```{ktvertmul}
{ }{3}{ }{ }
{ }{6}{5}{1}
{ }{ }{ }{6}
------------
{3}{9}{0}{6}
```

1.125)

```{ktlongdiv}
   {0704}
{7}{4928}
   {0}
   {\underline{49}}
   {49}
   {002}
   {\underline{000}}
   {0028}
   {\underline{0028}}
   {0000}
```

```{ktvertmul}
{ }{ }{2}{ }
{ }{7}{0}{4}
{ }{ }{ }{7}
------------
{4}{9}{2}{8}
```

1.126)

```{ktlongdiv}
   {0809}
{7}{5663}
   {\underline{0}}
   {56}
   {\underline{56}}
   {006}
   {\underline{000}}
   {0063}
   {\underline{0063}}
   {0000}
```

```{ktvertmul}
{ }{ }{6}{ }
{ }{8}{0}{9}
{ }{ }{ }{7}
------------
{5}{6}{6}{3}
```

1.127)

```{ktlongdiv}
   {0476R4}
{8}{3812}
   {\underline{0}}
   {38}
   {32}
   {\underline{061}}
   {056}
   {0052}
   {\underline{0048}}
   {0004}
```

```{ktvertmul}
{ }{6}{4}{ }
{ }{4}{7}{6}
{ }{ }{ }{8}
------------
{3}{8}{0}{8}
```

```{ktvertadd}
{ }{ }{1}{ }
{3}{8}{0}{8}
{ }{ }{ }{4}
------------
{3}{8}{1}{2}
```

1.128)

```{ktlongdiv}
   {0539R7}
{8}{4319}
   {\underline{0}}
   {43}
   {\underline{40}}
   {031}
   {\underline{024}}
   {0079}
   {\underline{0072}}
   {0007}
```

```{ktvertmul}
{ }{3}{7}{ }
{ }{5}{3}{9}
{ }{ }{ }{8}
------------
{4}{3}{1}{2}
```

```{ktvertmul}
{ }{ }{ }{ }
{4}{3}{1}{2}
{ }{ }{ }{7}
------------
{4}{3}{1}{9}
```

1.129)

```{ktlongdiv}
    {0114R11}
{13}{1493}
    {\underline{13}}
    {019}
    {\underline{013}}
    {0063}
    {\underline{0052}}
    {0011}
```

```{ktvertmul}
{ }{ }{1}{ }
{ }{1}{1}{4}
{ }{ }{1}{3}
------------
{ }{3}{4}{2}
{1}{1}{4}{0}
------------
{1}{4}{8}{2}
```

```{ktvertsub}
{1}{4}{9}{3}
{1}{4}{8}{2}
------------
{ }{ }{1}{1}
```

1.130)

```{ktlongdiv}
    {0121R9}
{12}{1461}
    {\underline{12}}
    {026}
    {\underline{024}}
    {0021}
    {\underline{0012}}
    {0009}
```

```{ktvertmul}
{ }{1}{2}{1}
{ }{ }{1}{2}
------------
{ }{2}{4}{2}
{1}{2}{1}{0}
------------
{1}{4}{5}{2}
```

```{ktvertsub}
{ }{ }{5}{11}
{1}{4}{6}{1}
{1}{4}{5}{2}
------------
{ }{ }{ }{9}
```

1.31)

```{ktlongdiv}
     {00300R41}
{256}{78641}
     {\underline{786}}
     {0004}
     {\underline{0000}}
     {00041}
     {\underline{00000}}
     {00041}
```

```{ktvertmul}
{ }{ }{1}{1}{ }
{ }{ }{2}{5}{6}
{ }{ }{3}{0}{0}
---------------
{ }{ }{0}{0}{0}
{ }{0}{0}{0}{0}
{7}{6}{8}{0}{0}
---------------
{7}{6}{8}{0}{0}
```

```{ktvertadd}
{7}{6}{8}{0}{0}
{ }{ }{ }{4}{1}
---------------
{7}{6}{8}{4}{1}
```

1.132)

```{ktlongdiv}
     {00308R77}
{248}{76461}
     {\underline{744}}
     {0206}
     {\underline{0000}}
     {02061}
     {\underline{01984}}
     {00077}
```

```{ktvertmul}
{ }{ }{1}{2}{ }
{ }{ }{3}{6}{ }
{ }{ }{2}{4}{8}
{ }{ }{3}{0}{8}
---------------
{ }{1}{9}{8}{4}
{ }{0}{0}{0}{0}
{7}{4}{4}{0}{0}
---------------
{7}{6}{3}{8}{4}
```

```{ktvertadd}
{ }{ }{1}{1}{ }
{7}{6}{3}{8}{4}
{ }{ }{ }{7}{7}
---------------
{7}{6}{4}{6}{1}
```

1.133) 91 / 13 = 7

1.134) 52 / 13 = 4

1.135) 135 / 9 = 15

1.136) 36 / 4 = 9

__EXERCISE__

1.5.343) fifty four divided by nine, quotient of fifty four and nine, nine divided into fifty four

1.5.344) fifty six divided by seven, quotient of fifty six and seven, seven divided into fifty six

1.5.345) thirty two divided by eight, quotient of thirty two and eight, eight divided into thirty two

1.5.346) forty two divided by six, quotient of forty two and six, six divided into forty two

1.5.347) forty eight divided by six, quotient of forty eight and six, six divided into forty eight

1.5.348) sixty three divided by nine, quotient of sixty three and nine, nine divided into sixty three

1.5.349) sixty three divided by seven, quotient of sixty three and seven, seven divided into sixty three

1.5.350) seventy two divided by eight, quotient of seventy two and eight, eight divided into seventy two

1.5.351)

```
□□□□□ □□□□□ □□□□□
  5     5     5
15 total
```

1.5.352)

```
□□□□□ □□□□□
  5     5  
10 total
```

1.5.353)

```
□□□□□□□ □□□□□□□
   7       7  
14 total
```

1.5.354)

```
□□□□□□ □□□□□□ □□□□□□
   6      6      6
18 total
```

1.5.355)

```
□□□□ □□□□ □□□□ □□□□ □□□□
  4   4    4    4    4
20 total
```

1.5.356)

```
□□□ □□□ □□□ □□□ □□□
 3   3   3   3   3
15 total
```

1.5.357)

```
□□□□□□ □□□□□□ □□□□□□ □□□□□□
   6     6      6      6
24 total
```

1.5.358)

```
□□□□ □□□□ □□□□ □□□□
  4   4    4    4
16 total
```

1.5.359) 18/2=9, 9*2=18

1.5.360) 14/2=7, 7*2=14

1.5.361) 27/3=9, 9*3=27

1.5.362) 30/3=10, 10*3=30

1.5.363) 28/4=7, 7*4=28

1.5.364) 36/4=9, 9*4=36

1.5.365) 45/5=9, 9*5=45

1.5.366) 35/5=7, 7*5=35

1.5.367) 72/8=9, 9*8=72

1.5.368) 64/8=8, 8*8=64

1.5.369) 35/7=5, 5*7=35

1.5.370) 42/7=6, 6*7=42

1.5.371) 15/15=1, 1*15=15

1.5.372) 12/12=1, 1*12=12

1.5.373) 43/43=1, 1*43=43

1.5.374) 37/37=1, 1*37=37

1.5.375) 23/1=23, 23*1=23

1.5.376) 29/1=29, 29*1=29

1.5.377) 19/1=19, 19*1=19

1.5.378) 17/1=17, 17*1=17

1.5.379) 0/4=0, 0*4=0

1.5.380) 0/8=0, 0*8=0

1.5.381) 5/0=undefined

1.5.382) 9/0=undefined

1.5.383) 26/0=undefined

1.5.384) 32/0=undefined

1.5.385) 0/12=0, 12*0=0

1.5.386) 0/36=0, 36*0=0

1.5.387) 72/3=24, 3*24=72

1.5.388)

```{ktlongdiv}
   {19}
{3}{57}
   {3}
   {27}
   {27}
   {00}
```

```{ktvertmul}
{ }{2}{ }
{ }{1}{9}
{ }{ }{3}
--
{ }{5}{7}
```

1.5.389)

```{ktlongdiv}
   {12}
{8}{96}
   {8}
   {16}
   {16}
   {00}
```

```{ktvertmul}
{ }{1}{ }
{ }{1}{2}
{ }{ }{8}
--
{ }{9}{6}
```

1.5.390)

```{ktlongdiv}
   {13}
{6}{78}
   {6}
   {18}
   {18}
   {00}
```

```{ktvertmul}
{ }{1}{ }
{ }{1}{3}
{ }{ }{6}
--
{ }{7}{8}
```

1.5.391)

```{ktlongdiv}
   {093}
{5}{465}
   {45}
   {015}
   {015}
   {000}
```

```{ktvertmul}
{ }{ }{1}{ }
{ }{ }{9}{3}
{ }{ }{ }{5}
--
{ }{4}{6}{5}
```

1.5.392)

```{ktlongdiv}
   {132}
{4}{528}
   {4}
   {12}
   {12}
   {008}
   {008}
   {000}
```

```{ktvertmul}
{ }{1}{ }{ }
{ }{1}{3}{2}
{ }{ }{ }{4}
--
{ }{5}{2}{8}
```

1.5.393)

```{ktlongdiv}
   {132}
{7}{924}
   {7}
   {22}
   {21}
   {014}
   {014}
   {000}
```

```{ktvertmul}
{ }{2}{1}{ }
{ }{1}{3}{2}
{ }{ }{ }{7}
--
{ }{9}{2}{4}
```

1.5.394)

```{ktlongdiv}
   {123}
{7}{861}
   {7}
   {16}
   {14}
   {021}
   {021}
   {000}
```

```{ktvertmul}
{ }{1}{2}{ }
{ }{1}{2}{3}
{ }{ }{ }{7}
--
{ }{8}{6}{1}
```

1.5.395)

```{ktlongdiv}
   {0871}
{6}{5226}
   {48}
   {04}
   {00}
   {042}
   {042}
   {0006}
   {0006}
   {0000}
```

```{ktvertmul}
{ }{4}{ }{ }
{ }{8}{7}{1}
{ }{ }{ }{6}
--
{5}{2}{2}{6}
```

1.5.396)

```{ktlongdiv}
   {0472}
{8}{3776}
   {32}
   {057}
   {056}
   {0016}
   {0016}
   {0000}
```

```{ktvertmul}
{ }{5}{1}{ }
{ }{4}{7}{2}
{ }{ }{ }{8}
--
{3}{7}{7}{6}
```

1.5.397)

```{ktlongdiv}
   {07831}
{4}{31324}
   {28}
   {033}
   {032}
   {0012}
   {0012}
   {00004}
```

```{ktvertmul}
{ }{3}{1}{ }{ }
{ }{7}{8}{3}{1}
{ }{ }{ }{ }{4}
--
{3}{1}{3}{2}{4}
```

1.5.398)

```{ktlongdiv}
   {09371}
{5}{46855}
   {45}
   {018}
   {015}
   {0035}
   {0035}
   {00005}
   {00005}
   {00000}
```

```{ktvertmul}
{ }{1}{3}{ }{ }
{ }{9}{3}{7}{1}
{ }{ }{ }{ }{5}
--
{4}{6}{8}{5}{5}
```

1.5.399)

```{ktlongdiv}
   {2403}
{3}{7209}
   {6}
   {12}
   {12}
   {000}
   {000}
   {0009}
   {0009}
   {0000}
```

```{ktvertmul}
{ }{1}{ }{ }{ }
{ }{2}{4}{0}{3}
{ }{ }{ }{ }{3}
--
{ }{7}{2}{0}{9}
```

1.5.400)

```{ktlongdiv}
   {1602}
{3}{4806}
   {3}
   {18}
   {18}
   {000}
   {000}
   {0006}
   {0006}
   {0000}
```

```{ktvertmul}
{ }{1}{ }{ }{ }
{ }{1}{6}{0}{2}
{ }{ }{ }{ }{3}
--
{ }{4}{8}{0}{6}
```

1.5.401)

```{ktlongdiv}
   {0901}
{6}{5406}
   {54}
   {000}
   {000}
   {0006}
   {0006}
   {0000}
```

```{ktvertmul}
{ }{ }{9}{0}{1}
{ }{ }{ }{ }{6}
--
{ }{5}{4}{0}{6}
```

1.5.402)

```{ktlongdiv}
   {0801}
{4}{3208}
   {32}
   {000}
   {000}
   {0008}
   {0008}
   {0000}
```

```{ktvertmul}
{ }{ }{8}{0}{1}
{ }{ }{ }{ }{4}
--
{ }{3}{2}{0}{4}
```

1.5.403)

```{ktlongdiv}
   {0704}
{4}{2816}
   {28}
   {001}
   {000}
   {0016}
   {0016}
   {0000}
```

```{ktvertmul}
{ }{ }{ }{1}{ }
{ }{ }{7}{0}{4}
{ }{ }{ }{ }{4}
--
{ }{2}{8}{1}{6}
```

1.5.404)

```{ktlongdiv}
   {0604}
{6}{3624}
   {36}
   {002}
   {000}
   {0024}
   {0024}
   {0000}
```

```{ktvertmul}
{ }{ }{ }{2}{ }
{ }{ }{6}{0}{4}
{ }{ }{ }{ }{6}
--
{ }{3}{6}{2}{4}
```

1.5.405)

```{ktlongdiv}
   {10209}
{9}{91881}
   {9}
   {01}
   {00}
   {018}
   {018}
   {0008}
   {0000}
   {00081}
   {00081}
   {00000}
```

```{ktvertmul}
{ }{1}{ }{8}{ }
{1}{0}{2}{0}{9}
{ }{ }{ }{ }{9}
--
{9}{1}{8}{8}{1}
```

1.5.406)

```{ktlongdiv}
   {10407}
{8}{83256}
   {8}
   {03}
   {00}
   {032}
   {032}
   {0005}
   {0000}
   {00056}
   {00056}
   {00000}
```

```{ktvertmul}
{ }{3}{ }{5}{ }
{1}{0}{4}{0}{7}
{ }{ }{ }{ }{8}
--
{8}{3}{2}{5}{6}
```

1.5.407)

```{ktlongdiv}
   {0410}
{7}{2470}
   {24}
   {007}
   {007}
   {0000}
```

```{ktvertmul}
{ }{ }{4}{1}{0}
{ }{ }{ }{ }{7}
--
{ }{2}{4}{7}{0}
```

1.5.408)

```{ktlongdiv}
   {0534R3}
{7}{3741}
   {35}
   {024}
   {021}
   {0031}
   {0028}
   {0003}
```

```{ktvertmul}
{ }{ }{2}{2}{ }
{ }{ }{5}{3}{4}
{ }{ }{ }{ }{7}
--
{ }{3}{7}{3}{8}
```

3738+3=3741

1.5.409)

```{ktlongdiv}
   {06913R1}
{8}{55305}
   {48}
   {073}
   {072}
   {0010}
   {0008}
   {00025}
   {00024}
   {00001}
```

```{ktvertmul}
{ }{7}{1}{2}{ }
{ }{6}{9}{1}{3}
{ }{ }{ }{ }{8}
--
{5}{5}{3}{0}{4}
```

55304+1=55305

1.5.410)

```{ktlongdiv}
   {05721R3}
{9}{51492}
   {45}
   {064}
   {063}
   {0019}
   {0018}
   {00012}
   {00009}
   {00003}
```

```{ktvertmul}
{ }{6}{1}{ }{ }
{ }{5}{7}{2}{1}
{ }{ }{ }{ }{9}
--
{5}{1}{4}{8}{9}
```

51489+3=51492

1.5.411)

```{ktlongdiv}
   {086234R4}
{5}{431174}
   {40}
   {031}
   {030}
   {0011}
   {0010}
   {00017}
   {00015}
   {000024}
   {000020}
   {000004}
```

```{ktvertmul}
{ }{ }{3}{1}{1}{2}{ }
{ }{ }{8}{6}{2}{3}{4}
{ }{ }{ }{ }{ }{ }{5}
--
{ }{4}{3}{1}{1}{7}{0}
```

431170+4=431174

1.5.412)

```{ktlongdiv}
   {074319R1}
{4}{297277}
   {28}
   {017}
   {016}
   {0012}
   {0012}
   {00007}
   {00004}
   {000037}
   {000036}
   {000001}
```

```{ktvertmul}
{ }{ }{1}{1}{ }{3}{ }
{ }{ }{7}{4}{3}{1}{9}
{ }{ }{ }{ }{ }{ }{4}
--
{ }{2}{9}{7}{2}{7}{6}
```

297276+1=29727

1.5.413)

```{ktlongdiv}
   {043338R2}
{3}{130016}
   {12}
   {010}
   {009}
   {0010}
   {0009}
   {00011}
   {00009}
   {000026}
   {000024}
   {000002}
```

```{ktvertmul}
{ }{ }{1}{1}{1}{2}{ }
{ }{ }{4}{3}{3}{3}{8}
{ }{ }{ }{ }{ }{ }{3}
--
{ }{1}{3}{0}{0}{1}{4}
```

130014+2=130016

1.5.414)

```{ktlongdiv}
   {052804R1}
{2}{105609}
   {10}
   {005}
   {004}
   {0016}
   {0016}
   {00000}
   {00000}
   {000009}
   {000008}
   {000001}
```

```{ktvertmul}
{ }{ }{ }{1}{ }{ }{ }
{ }{ }{5}{2}{8}{0}{4}
{ }{ }{ }{ }{ }{ }{2}
--
{ }{1}{0}{5}{6}{0}{8}
```

105608+1=105609

1.5.415)

```{ktlongdiv}
    {0382R5}
{15}{5735}
    {45}
    {123}
    {120}
    {0035}
    {0030}
    {0005}
```

```{ktvertmul}
{ }{ }{ }{ }{ }{ }{ }
{ }{ }{ }{ }{4}{1}{ }
{ }{ }{ }{ }{3}{8}{2}
{ }{ }{ }{ }{ }{1}{5}
--
{ }{ }{ }{1}{9}{1}{0}
{ }{ }{ }{3}{8}{2}{0}
--
{ }{ }{ }{5}{7}{3}{0}
```

5730+5=5735

1.5.416)

```{ktlongdiv}
    {0234R19}
{21}{4933}
    {42}
    {073}
    {063}
    {0103}
    {0084}
    {0019}
```

```{ktvertmul}
{ }{ }{ }{ }{2}{3}{4}
{ }{ }{ }{ }{ }{2}{1}
--
{ }{ }{ }{ }{2}{3}{4}
{ }{ }{ }{4}{6}{8}{0}
--
{ }{ }{ }{4}{9}{1}{4}
```

4914+19=4933

1.5.417)

```{ktlongdiv}
    {00849}
{67}{56883}
    {536}
    {0328}
    {0268}
    {00603}
    {00603}
    {00000}
```

```{ktvertmul}
{ }{ }{ }{ }{2}{5}{ }
{ }{ }{ }{ }{3}{6}{ }
{ }{ }{ }{ }{8}{4}{9}
{ }{ }{ }{ }{ }{6}{7}
--
{ }{ }{ }{5}{9}{4}{3}
{ }{ }{5}{0}{9}{4}{0}
--
{ }{ }{5}{6}{8}{8}{3}
```

1.5.418)

```{ktlongdiv}
    {00583}
{75}{43725}
    {375}
    {0622}
    {0600}
    {00225}
    {00225}
    {00000}
```

```{ktvertmul}
{ }{ }{ }{ }{5}{2}{ }
{ }{ }{ }{ }{4}{1}{ }
{ }{ }{ }{ }{5}{8}{3}
{ }{ }{ }{ }{ }{7}{5}
--
{ }{ }{ }{2}{9}{1}{5}
{ }{ }{4}{0}{8}{1}{0}
--
{ }{ }{4}{3}{7}{2}{5}
```

1.5.419)

```{ktlongdiv}
     {00096}
{314}{30144}
     {2826}
     {01884}
     {01884}
     {00000}
```

```{ktvertmul}
{ }{ }{ }{ }{1}{3}{ }
{ }{ }{ }{ }{ }{2}{ }
{ }{ }{ }{ }{3}{1}{4}
{ }{ }{ }{ }{ }{9}{6}
--
{ }{ }{ }{1}{8}{8}{4}
{ }{ }{2}{8}{2}{6}{0}
--
{ }{ }{3}{0}{1}{4}{4}
```

1.5.420)

```{ktlongdiv}
     {00063}
{415}{26145}
     {2490}
     {01245}
     {01245}
     {00000}
```

```{ktvertmul}
{ }{ }{ }{ }{ }{3}{ }
{ }{ }{ }{ }{ }{1}{ }
{ }{ }{ }{ }{4}{1}{5}
{ }{ }{ }{ }{ }{6}{3}
--
{ }{ }{ }{1}{2}{4}{5}
{ }{ }{2}{4}{9}{0}{0}
--
{ }{ }{ }{ }{ }{ }{ }
{ }{ }{2}{6}{1}{4}{5}
```

1.5.421)

```{ktlongdiv}
     {001986R17}
{273}{542195}
     {273}
     {2691}
     {2457}
     {02349}
     {02184}
     {001655}
     {001638}
     {000017}
```

```{ktvertmul}
{ }{ }{ }{ }{ }{ }{ }
{ }{ }{ }{1}{1}{1}{ }
{ }{ }{ }{6}{6}{4}{ }
{ }{ }{ }{2}{2}{1}{ }
{ }{ }{ }{1}{9}{8}{6}
{ }{ }{ }{ }{2}{7}{3}
--
{ }{ }{ }{5}{9}{5}{8}
{ }{1}{3}{9}{0}{2}{0}
{ }{3}{9}{7}{2}{0}{0}
--
{ }{5}{4}{2}{1}{7}{8}
```

542178+17=542195

1.5.422)

```{ktlongdiv}
     {001766R351}
{462}{816243}
     {462}
     {3542}
     {3234}
     {03084}
     {02772}
     {003123}
     {002772}
     {000351}
```


```{ktvertmul}
{ }{ }{ }{3}{2}{2}{ }
{ }{ }{ }{4}{3}{3}{ }
{ }{ }{ }{1}{1}{1}{ }
{ }{ }{ }{1}{7}{6}{6}
{ }{ }{ }{ }{4}{6}{2}
--
{ }{ }{ }{3}{5}{3}{2}
{ }{1}{0}{5}{9}{6}{0}
{ }{7}{0}{6}{4}{0}{0}
--
{ }{8}{1}{5}{8}{9}{2}
```

815892+351=816243

1.5.423)

```{ktvertmul}
{ }{ }{2}{ }
{ }{2}{0}{4}
{ }{ }{1}{5}
--------
{1}{0}{2}{0}
{2}{0}{4}{0}
-----
{3}{0}{6}{0}
```

1.5.424)

```{ktvertmul}
{ }{ }{6}{ }{ }
{ }{ }{3}{ }{ }
{ }{ }{3}{9}{1}
{ }{ }{ }{7}{4}
--
{ }{1}{5}{6}{4}
{2}{7}{3}{7}{0}
--
{2}{8}{9}{3}{4}
```

1.5.425)

```{ktvertsub}
{1}{15}{ }
{2}{5 }{6}
{1}{8 }{4}
--
{0}{7}{2}
```

1.5.426)

```{ktvertsub}
{2}{10}{ }
{3}{ 0}{5}
{2}{ 6}{2}
--
{0}{4}{3}
```

1.5.427)

```{ktvertadd}
{ }{ }{1}{ }
{ }{7}{1}{9}
{ }{3}{4}{1}
--
{1}{0}{6}{0}
```

1.5.428)

```{ktvertadd}
{ }{ }{1}{ }
{ }{6}{4}{7}
{ }{5}{2}{8}
---
{1}{1}{7}{5}
```

1.5.429)

```{ktlongdiv}
    {035}
{25}{875}
    {75}
    {125}
    {125}
    {000}
```

1.5.430)

```{ktlongdiv}
    {0048}
{23}{1104}
    {092}
    {0184}
    {0184}
    {0000}
```

1.5.431) 45/15=3

1.5.432) 64/16=4

1.5.433) 288/24=12

1.5.434) 256/32=8

1.5.435) 64/2=32

1.5.436) 42/3=14

1.5.437) 125/5=25

1.5.438) 152/8=19

1.5.439) 48/3=16

1.5.440) 54/2=28

1.5.441) 45-17=28

1.5.442) 71-53=18

1.5.443) 45/9=5

1.5.444) 128/4=32

1.5.445) 8+14+11+17=50

1.5.446) 6+26+15+9=56

1.5.447) 12*4=48

1.5.448) 14*5=120

1.5.449) one is the inverse of another.

long division seems to be the inverse of vertical multiplication.
* in long division you're going from left to right and subtracting.
* in vertical multiplication you're going from right to left and adding.

1.5.450) multiple 8 by 37 and add 4, the result should be 800

1.5.451) 

```{ktlongdiv}
    {026R1}
{14}{365}
    {28}
    {085}
    {084}
    {001}
```

1.5.452)

```{ktlongdiv}
    {014R15}
{25}{365}
    {25}
    {115}
    {100}
    {015}
```

## Chapter 2 Section 2.1

__TRY IT__

2.1)

* a) 18 plus 11; the sum of 18 and 11
* b) 27 times 9; the product of 27 and 9
* c) 84 divided by 7; the quotient of 84 and 7; 7 divided into 84
* d) p minus q; the difference of p and q; q subtracted from 9

2.2)

* a) 47 minus 9; the difference of 47 and 9; 9 subtracted from 47
* b) 72 divided by 9; the quotient of 72 and 9; 9 divided into 72
* c) m plus n; the sum of m and n
* d) 13 times 7; the product of 7 and 9

2.3)

* a) 14 is less than or equal to 27
* b) 19 minus 2 is not equal to 8
* c) 12 is greater than 4 divided by 2
* d) x minus 7 is less than 1

2.4)

* a) 19 is greater than or equal to 15
* b) 7 is equal to 12 minus 5
* c) 15 divided by 3 is less than 8
* d) y minus 3 is greater than 6

2.5)

* a) 48 > 26
* b) 27 < 28

2.6)

* a) 27 < 48
* b) 28 > 27

2.7)

* a) 23 + 6 = 29 -- equation
* b) 7 * 3 - 7 -- expression

2.8)

* a) y/14 -- expression
* b) x - 6 = 21 -- equation

2.9) `{kt} {41}^5`

2.10) `{kt} {7}^9`

2.11)

* a) 4\*4\*4\*4\*4\*4\*4\*4
* b) a\*a\*a\*a\*a\*a\*a

2.12)

* a) 8\*8\*8\*8\*8\*8\*8\*8
* b) b\*b\*b\*b\*b\*b

2.13)

* a) 5\*5\*5
* b) 1\*1\*1\*1\*1\*1\*1

2.14)

* a) 7\*7
* b) 0\*0\*0\*0\*0

2.15)

* a) 12-5\*2 = 12-10 = 2
* b) (12-5)\*2 = 7\*2 = 14

2.16)

* a) 8+3\*9 = 8+27 = 35
* b) (8+3)\*9 = 11\*9 = 99

2.17) 42/7\*3 = 6\*3 = 18

2.18) 12\*3/4 = 36/4 = 9

2.19) 30/5+10(3-2) = 30/5+10(1) = 30/5+10(1) = 6+10(1) = 6+10 = 16

2.20) 70/10+4(6-2) = 70/10+4(4) = 7/1+4(4) = 7+4(4) = 7+16 = 23

2.21) 9+5^3-(4(9+3)) = 9+5^3-(4(11)) = 9+5^3-(44) = 9+5^3-44 = 9+125-44 = 134-44 = 90

2.22) 7^2-2(4(5+1)) = 7^2-2(4(6)) = 7^2-2(24) = 49-2(24) = 49-48 = 1

2.23) 3^2 + 2^4 / 2 + 4^3 = 9+16/2+48 = 9+8+48 = 17+48 = 65

2.24) 6^2 - 5^3 / 5 + 8^2 = 36 - 125 / 5 + 64 = 36-25+64 = 61+64 = 125

__EXERCISE__

2.1.1) 16 minus 9; difference of 16 and 9; subtract 9 from 16

2.1.2) 25 minus 7; difference of 27 and 7; subtract 7 from 25

2.1.3) 5 times 6; product of 5 and 6; 5 multiplied by 6

2.1.4) 3 times 9; product of 3 and 9; 3 multiplied by 9

2.1.5) 28 divided by 4; quotient of 24 and 8; 24 divided by 8; 24 divided into 8

2.1.6) 45 divided by 5; quotient of 45 and 5; 45 divided bt 5; 5 divided into 45

2.1.7) x plus 8; sum of x and 8

2.1.8) x plus 11; sum of x and 11

2.1.9) 2 times 7; product of 2 and 7

2.1.10) 4 times 8; product of 4 and 8

2.1.11) 14 is less than 21

2.1.12) 17 is less than 35

2.1.13) 36 is greater than or equal to 19

2.1.14) 42 is greater than or equal to 27

2.1.15) 3 times n is equal to 24

2.1.16) 6 times n is equal to 36

2.1.17) y minus 1 is greater than 6

2.1.18) y minus 4 is greater than 8

2.1.19) 2 is less than or equal to 18 divided by 6

2.1.20) 3 is less than or equal to 20 divided by 4

2.1.21) a is not equal to 7 times 4

2.1.22) a is not equal to 1 times 12

2.1.23) equation

2.1.24) equation

2.1.25) expression

2.1.26) expression

2.1.27) expression

2.1.28) expression

2.1.29) equation

2.1.30) expression

2.1.31) 3^7

2.1.32) 4^6

2.1.33) x^5

2.1.34) y^6

2.1.35) 5\*5\*5

2.1.36) 8\*8\*8

2.1.37) 2\*2\*2\*2\*2\*2\*2\*2

2.1.38) 10\*10\*10\*10\*10

2.1.39)

* a) 3+8\*5 = 3+40 = 43
* b) (3+8)\*5 = 11\*5 = 55

2.1.40)

* a) 2+6\*3 = 2+18 = 20
* b) (2+6)\*3 = 8\*3 = 24

2.1.41) 2^3-12/(9-5) = 2^3-12/4 = 8-12/4 = 8-3 = 5

2.1.42) 3^2-18/(11-5) = 3^2-18/6 = 9-18/6 = 9-3 = 6

2.1.43) 3\*8+5\*2 = 3\*8+10 = 3\*8+10 = 24+10 = 34

2.1.44) 4\*7+3\*5 = 28+3\*5 = 28+15 = 43

2.1.45) 2+8(6+1) = 2+8(7) = 2+56 = 58

2.1.46) 4+6(3+6) = 4+6(9) = 4+54 = 58

2.1.47) 4\*12/8 = 48/8 = 6

2.1.48) 2\*36/6 = 2\*6 = 12

2.1.49) 6+10/2+2 = 6+5+2 = 13

2.1.50) 9+12/3+4 = 9+4+4 = 17

2.1.51) (6+10)/(2+2) = 16/4 = 4

2.1.52) (9+12)/(3+4) = 21/7 = 3

2.1.53) 20/4+6\*5 = 5+30 = 35

2.1.54) 33/3+8\*2 = 11+16 = 27

2.1.55) 20/(4+6)\*5 = 20/10\*5 = 2\*5 = 10

2.1.56) 33/(3+8)\*2 = 33/11\*2 = 3\*2 = 6

2.1.57) 4^2+5^2 = 16+25 = 41

2.1.58) 3^2+7^2 = 9+49 = 58

2.1.59) (4+5)^2 = 9^2 = 81

2.1.60) (3+7)^2 = 10^2 = 100

2.1.61) 3(1+9\*6)-4^2 = 3(1+54)-4^2 = 3\*55-4^2 = 3\*55-16 = 165

2.1.62) 5(2+8\*4)-7^2 = 5(2+32)-7^2 = 5\*34-7^2 = 5\*34-49 = 170-49 = 121

2.1.63) 2(1+3(10-2)) = 2(1+3(8)) = 2(1+24) = 2\*25 = 50

2.1.64) 5(2+4(3-2)) = 5(2+4(1)) = 5(2+4) = 5(6) = 40

2.1.65)

* a) >
* b) =
* c) <
* d) <
* e) >

2.1.66)

* a) >
* b) <
* c) <
* d) >
* e) >

2.1.67) expression is a hierarchy of math operations, evaluation is the relationship between 2 expressions

2.1.68) it's so simplifying an expression always results in the same answer

## Chapter 2 Section 2.2

__TRY IT__

2.25) y+4

* a) y=6, 6+4=10
* b) y=15, 15+4=19

2.26) a-5

* a) a=9, 9-5=4
* b) a=17, 17-5=12

2.27) 8x-3

* a) x=2, 8(2)-3=13
* b) x=1, 8(1)-3=5

2.28) 4y-4

* a) y=3, 4(3)-4=8
* b) y=5, 4(5)-4=16

2.29) x^2 -- when x=8, 8^2=64

2.30) x^3 -- when x = 6, 6^3=108

2.31) 2^x -- when x = 6, 2^6=64

2.32) 3^x -- when x = 4, 3^4=81

2.33) 2x+5y-4 -- when x = 11 and y = 13, 2(11)+5(4)-4 = 22+20-4 = 22+16 = 38

2.34) 5x-2y-9 -- when x = 7 and y = 8, 5(7)-2(8)-9 = 35-16-9 = 35-7 = 28

2.35) 3x^2+4x+1 -- x=3, 3(3)^2+4(3)+1 = 3(9)+4(3)+1 = 27+12+1 = 27+13 = 40

2.36) 6x^2-4x-7 -- x=2, 6(2)^2-4(2)-7 = 6(4)-4(2)-7 = 24-8-7 = 23

2.37) 4x + 3b + 2 has the terms...

* 4x with a coefficient of 4
* 3b with a coefficient of 3
* 2 with a coefficient of 2 (this book says that a constant by itself is considered a coefficient but all other resources are saying that it isn't)

2.38) 9a + 13a^2 + a^3 has the terms 9a, 13a^2, a^3

* 9a with a coefficient of 9
* 13a^2 with a coefficient of 13
* a^3 with a coefficient of 3 (a^3 is the same as 1*a^3)

2.39) like terms in 9, 2x^3, y^2, 8x^3, 15, 9y, 11y^2...

* 9 and 15
* 2x^3 and 8x^3
* y^2 and 11y^2

2.40) like terms in the expression 4x^3+8x^2+19+3x^2+24+6x^3 ...

* 4x^3 and 6x^3
* 8x^2 and 3x^2
* 19 and 24

2.41) 7x+9+9x+8 simplifies to 16x+17

2.42) 5y+2+8y+4y+5 simplifies to 17y+7

2.43) 3x^2+9x+x^2+5x simplifies to 4x^2+14x

2.44) 11y^2+8y+y^2+7y simplifies to 12y^2+15y

2.45)

* a) 47-41
* b) 5x/2

2.46)

* a) 17+19
* b) 7x

2.47)

* a) x+11
* b) 11a-14

2.48)

* a) j + 19
* b) 2x - 21

2.49)

* a) 4(p+q)
* b) 4p+q

2.50)

* a) 2x-8
* b) 2*(x-8)

2.51) l = w-5

2.52) w = 2 + l

2.53) d = 5q-7

2.54) d = 8 + 4n

__EXERCISE__

2.2.69) 7(2)+8 = 14+8 = 22

2.2.70) 9(3)+7 = 27+7 = 34

2.2.71) 5(6)-4 = 30-4 = 26

2.2.72) 8(7)-6 = 56-6 = 50

2.2.73) 12^2 = 144

2.2.74) 5^3 = 125

2.2.75) 2^5 = 32

2.2.76) 3^4 = 81

2.2.77) 3^3 = 27

2.2.78) 4^2 = 16

2.2.79) 4^2 + 3*4 - 7 = 16 + 12 - 7 = 28 - 7 = 21

2.2.80) 6^2 + 5*6 - 8 = 36 + 30 - 8 =  66 - 8 = 58

2.2.81) 2\*7 + 4\*8 - 5 = 14 + 32 - 9 = 46 - 9 = 37

2.2.82) 6\*6 + 3\*9 - 9 = 36 + 27 - 9 = 36 + 18 = 54

2.2.83) (10-7)^2 = 3^2 = 9

2.2.84) (6+9)^2 = 15^2 = 225

2.2.85) 3^2 + 8^2 = 9 + 64 = 73

2.2.86) 12^2 - 5^2 = 144 - 25 = 119

2.2.87) 2(15) + 2(12) = 30 + 24 = 54

2.2.88) 2(18) + 2(14) = 36 + 28 = 64

2.2.89) 15x^2, 6x, 2

2.2.90) 11x^2, 8x, 5

2.2.91) 10y^3, y, 2

2.2.92) 9y^3, y, 5

2.2.93) 8

2.2.94) 13

2.2.95) 5

2.2.96) 6

2.2.97) {x^3, 8x^3}, {8x}, {14, 5}, {8y}

2.2.98) {6z, 4z}, {3w^2, w^2}, {1}, {6z^2}

2.2.99) {9a}, {a^2}, {16ab, 4ab}, {16b^2, 9b^2}

2.2.100) {3}, {25r^2, 4r^2}, {10s, 3s}, {10r}

2.2.101) 13x

2.2.102) 19x

2.2.103) 26a

2.2.104) 27z

2.2.105) 7c

2.2.106) 11y

2.2.107) 12x+8

2.2.108) 13a+9

2.2.109) 10u+3

2.2.110) 10d+11

2.2.111) 12p+10

2.2.112) 12x-2

2.2.113) 22a+1

2.2.114) 22c+0=22c

2.2.115) 17x^2+20x+16

2.2.116) 7b^2+12b+6

2.2.117) 8+12

2.2.118) 9+1

2.2.119) 14-9

2.2.120) 19-8

2.2.121) 9*7

2.2.122) 8*7

2.2.123) 36/9

2.2.124) 42/7

2.2.125) x-4

2.2.126) x-3

2.2.127) 6*y

2.2.128) 9*y

2.2.129) 8x+3x

2.2.130) 13x+3x

2.2.131) y/3

2.2.132) y/8

2.2.133) 8*(y-9)

2.2.134) 7*(y-1)

2.2.135) 5*(x+y)

2.2.136) 2x-(9*5)

2.2.137) s = b + 15

2.2.138) r = 3 + c

2.2.139) g = b - 4

2.2.140) m = f - 6

2.2.141) p = 2n-7

2.2.142) f = 3+6t

2.2.143) justin pays 750, insurance company pays 2100-750

2.2.144) pam and armando pay 2500, insurance pays 19400-2500

2.2.145) addition has commutative property, subtraction doesn't

2.2.146) the operators in each expression are different -- 4(x+y) vs 4x+y

## Chapter 2 Section 2.3

__TRY IT__

2.55)

* 4(3)-7 = 12-7 = 5
* 5 != 16

2.56)

* 6(2)-2 = 12-2 = 10
* 10 = 10

2.57)

* 9(3)-2 = 27-2 = 25
* 8(3)=1 = 24+1 = 25
* 25 = 25

2.58)

* 5(4)-3 = 20-3 = 17
* 3(4)+5 = 12+5 = 17
* 17 = 17

2.59) x+1=7

2.60) x+3=4

2.61) 

* x+6 = 19
* x+6-6 = 19-6
* x=13

2.62)

* x+9 = 14
* x+9-9 = 14-9
* x = 5

2.63)

* 95 = y+67
* 95-67 = y+67-67
* 28 = y

2.64)

* 91 = y+45
* 91-45 = y+45-45
* 46 = y

2.65)

* x-9 = 13
* x-9+9 = 13+9
* x = 22

2.66)

* y-1 = 3
* y-1+1 = 3+1
* y = 4

2.67)

* 19 = a-18
* 19+18 = a-18+18
* 37 = a

2.68)

* 27=n-14
* 27+14=n-14+14
* 41=n

2.69) 7+6=13

2.70) 8+6=14

2.71) 6*9=54

2.72) 21*3=63

2.73) 2(x-5)=30

2.74) 2(y-4)=16

2.75)

* 7+x = 37
* 7+x-7 = 37-7
* x = 30

2.76)

* 11+y = 28
* 11+y-11 = 28-11
* y = 17

2.77)

* z-7 = 37
* z-7+7 = 37+7
* z = 44

2.78)

* x-19 = 45
* x-19+19 = 45+19
* x = 64

__EXERCISE__

2.3.147) a

2.3.148) a

2.3.149) b

2.3.150) b

2.3.151) a

2.3.152) a

2.3.153) b

2.3.154) b

2.3.155) b

2.3.156) b

2.3.157) b

2.3.158) b

2.3.159) x+2=5

2.3.160) 4+x=7

2.3.161) 3+x=6

2.3.162) 5+x=9

2.3.163)

* a+2=18
* a+2-2=18-2
* a=16

2.3.164)

* b+5=13
* b+5-5=13-5
* b=8

2.3.165)

* p+18=23
* p+18-18=23-18
* p=5

2.3.166)

* q+14=31
* q+14-14=31-14
* q=17

2.3.167)

* r+76=100
* r+76-76=100-76
* r=24

2.3.168)

* s+62=95
* s+62-62=95-62
* s=33

2.3.169)

* 16=x+9
* 16-9=x+9-9
* 7=x

2.3.170)

* 17=y+6
* 17-6=y+6-6
* 11=y

2.3.171)

* 93=p+24
* 93-24=p+24-24
* 69=p

2.3.172)

* 116=q+79
* 116-79=q+79-79
* 37=q

2.3.173)

* 465=d+398
* 465-398=d+398-398
* 67=d

2.3.174)

* 932=c+641
* 932-641=c+641-641
* 291=c

2.3.175)

* y-3=19
* y-3+3=19+3
* y=21

2.3.176)

* x-4=12
* x-4+4=12+4
* x=16

2.3.177)

* u-6=24
* u-6+6=24+6
* u=30

2.3.178)

* v-7=35
* v-7+7=35+7
* v=42

2.3.179)

* f-55=123
* f-55+55=123+55
* f=178

2.3.180)

* g-39=117
* g-39+39=117+39
* g=156

2.3.181)

* 19=n-13
* 19+13=n-13+13
* 32=n

2.3.182)

* 18=m-15
* 18+15=m-15+15
* 33=m

2.3.183)

* 10=p-38
* 10+38=p-38+38
* 48=p

2.3.184)

* 18=q-72
* 18+72=q-72+72
* 90=q

2.3.185)

* 268=y-199
* 268+199=y-199+199
* 467=y

2.3.186)

* 204=z-149
* 204+149=z-149+149
* 353=z

2.3.187) 8+9=17

2.3.188) 7+9=16

2.3.189) 23-19=4

2.3.190) 29-12=17

2.3.191) 3*9=27

2.3.192) 6*8=48

2.3.193) 54/6=9

2.3.194) 42/7=6

2.3.195) 2(n-10)=52

2.3.196) 2(m-14)=64

2.3.197) (3y)+10=100

2.3.198) (8x)+4=68

2.3.199)

* 5+p=21
* 5+p-5=21-5
* p=16

2.3.200)

* 9+q=40
* 9+q-9=40-9
* q=31

2.3.201)

* r+18=73
* r+18-18=73-18
* r=55

2.3.202)

* s+13=68
* s+13-13=68-13
* s=55

2.3.203)

* d-30=52
* d-30+30=52+30
* d=82

2.3.204)

* c-25=75
* c-25+25=75+25
* c=100

2.3.205)

* u-12=89
* u-12+12=89+12
* u=101

2.3.206)

* w-19=56
* w-19+19=56+19
* w=75

2.3.207)

* c-325=799
* c-325+325=799+325
* c=1124

2.3.208)

* d-299=850
* d-299+299=850+299
* d=1149

2.3.209)

* 500+p=1800
* 500+p-500=1800-500
* p=1300

2.3.210)

* d-750=5800
* d-750+750=5800+750
* d=6550

2.3.211)

* p-120=340
* p-120+120=340+120
* p=460

2.3.212)

* 1299+t=1409
* 1299+t-1299=1409-1299
* t=110

2.3.213)

* 8x-2=16-6x
* 8x-6x-2=16-6x-6x
* 2x-2=16
* 2x-2+2=16+2
* 2x=18

no -- 2*1 != 18

2.3.214)

the difference of y and 5 is 21 -- NAME had paid 21 dollars in total for PRODUCT after receiving a 5 dollar discount. What was the original price of PRODUCT?

## Chapter 2 Section 2.4

__TRY IT__

2.79)

* a) is multiple of 2
* b) is not multiple of 2

2.80)

* a) is not multiple of 2
* b) is multiple of 2

2.81)

* a) is a multiple of 5
* b) is not a multiple of 5

2.82)

* a) is not multiple of 5
* b) is multiple of 5

2.83)

* a) is not multiple of 10
* b) is multiple of 10

2.84)

* a) is multiple of 10
* b) is not multiple of 10

2.85)

* a)
  * 9+5+4=18
  * 1+8=9
  * 9 is a multiple of 3
* b)
  * 3+7+4+2=16
  * 1+6=7
  * 7 is not a multiple of 3

2.86)

* a)
  * 6+4+3=13
  * 1+3=4
  * 4 is not a multiple of 3
* b)
  * 8+3+7+9=27
  * 2+7=9
  * 9 is a multiple of 3

2.87) 6240
 * divisible by 2: yes, last digit is 0
 * divisible by 5: yes, last digit is 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 6+2+4+0=12, yes digits sum to multiple of 3

2.88) 7248
 * divisible by 2: yes, last digit is 8
 * divisible by 5: no, last digit is not 5 or 0
 * divisible by 10: no, last digit is not 0
 * divisible by 3: 7+2+4+8=21, yes digits sum to multiple of 3

2.89) 4962
 * divisible by 2: yes, last digit is 2
 * divisible by 5: no, last digit is not 5 or 0
 * divisible by 10: no, last digit is not 0
 * divisible by 3: 4+9+6+2=21, yes digits sum to multiple of 3

2.90) 3765
 * divisible by 2: no, last digit is not 2,4,6, or 8
 * divisible by 5: yes, last digit is 5
 * divisible by 10: no, last digit is not 0
 * divisible by 3: 3+7+6+5=21, yes digits sum to multiple of 3

2.91)

* 96/1=96
* 96/2=48
* 96/3=23
* 96/4=14
* 96/5
* 96/6=16
* 96/7
* 96/8=12
* 96/9
* 96/10
* 96/11
* 96/12=8 <-- quotient is less than divisor, stop here because it'll just mirror after this point

2.92)

* 80/1=80
* 80/2=40
* 80/3
* 80/4=20
* 80/5=16
* 80/6
* 80/7
* 80/8=10
* 80/9
* 80/10=8 <-- quotitent is less than divisor, stop here

2.93)

* 91/1=91
* 91/2=50.5
* 91/3=30.333
* 91/4=2.75
* 91/5=18.2
* 91/6=15.1666
* 91/7=13 <-- stop here, it's composite because this will be the third factor (we know that 1 and 91 are factors already)

2.94)

* 137/1=137
* 137/2=68.5
* 137/3=45.666
* 137/4=34.25
* 137/5=27.4
* 137/6=22.8333
* 137/7=19.571
* 137/8=17.125
* 137/9=15.222
* 137/10=13.7
* 137/11=12.4545
* 137/12=11.41

__EXERCISE__

2.4.215)

1. 2
1. 4
1. 6
1. 8
1. 10
1. 12
1. 14
1. 16
1. 18
1. 20
1. 22
1. 24
1. 26
1. 28
1. 30
1. 32
1. 34
1. 36
1. 38
1. 40
1. 42
1. 44
1. 46
1. 48

2.4.216)

1. 3
1. 6
1. 9
1. 12
1. 15
1. 18
1. 21
1. 24
1. 27
1. 30
1. 33
1. 36
1. 39
1. 42
1. 45
1. 48

2.4.217)

1. 4
1. 8
1. 12
1. 16
1. 20
1. 24
1. 28
1. 32
1. 36
1. 40
1. 44
1. 48

2.4.218)

1. 5
1. 10
1. 15
1. 20
1. 25
1. 30
1. 35
1. 40
1. 45

2.4.219)

1. 6
1. 12
1. 18
1. 24
1. 30
1. 36
1. 42
1. 48

2.4.220)

1. 7
1. 14
1. 21
1. 28
1. 35
1. 42
1. 49

2.4.221)

1. 8
1. 16
1. 24
1. 32
1. 40
1. 48

2.4.222)

1. 9
1. 18
1. 27
1. 36
1. 45

2.4.223)

1. 10
1. 20
1. 30
1. 40

2.4.224)

1. 12
1. 24
1. 36
1. 48

2.4.225) 84

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: no, last digit is NOT 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 8+4=12, yes digits sum to multiple of 3
 * divisible by 6: yes because divisible by both 2 and 3

2.4.226) 96

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: no, last digit is NOT 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 9+6=15, yes digits sum to multiple of 3
 * divisible by 6: yes because divisible by both 2 and 3

2.4.227) 75

 * divisible by 2: no, last digit is NOT 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 7+5=12, yes digits sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.228) 78

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: no, last digit is NOT 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 7+8=15, yes digits sum to multiple of 3
 * divisible by 6: yes, divisible by both 2 and 3

2.4.229) 168

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: no, last digit is NOT 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 1+6+8=15, yes digits sum to multiple of 3
 * divisible by 6: yes, divisible by both 2 and 3

2.4.230) 264

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: no, last digit is NOT 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 2+6+4=12, yes digits sum to multiple of 3
 * divisible by 6: yes, divisible by both 2 and 3

2.4.231) 900

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 9+0+0=9, yes digits sum to multiple of 3
 * divisible by 6: yes, divisible by both 2 and 3

2.4.232) 800

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 8+0+0=8, no digits DONT sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.233) 896

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: no, last digit is NOT 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 8+9+6=23, no digits DONT sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.234) 942

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: no, last digit is NOT 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 9+4+2=15, yes digits sum to multiple of 3
 * divisible by 6: yes, divisible by both 2 and 3

2.4.235) 375

 * divisible by 2: no, last digit is NOT 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 3+7+5=15, yes digits sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.236) 750

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 7+5+0=12, yes digits sum to multiple of 3
 * divisible by 6: yes, divisible by both 2 and 3

2.4.237) 350

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 3+5+0=8, no digits DONT sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.238) 550

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 5+5+0=10, no digits DONT sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.239) 1430

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 1+4+3+0=8, no digits DONT sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.240) 1080

 * divisible by 2: yes, last digit is 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: yes, last digit is 0
 * divisible by 3: 1+0+8+0=9, yes digits sum to multiple of 3
 * divisible by 6: yes, divisible by both 2 and 3

2.4.241) 22335

 * divisible by 2: no, last digit is NOT 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 2+2+3+3+5=15, yes digits sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.242) 39075

 * divisible by 2: no, last digit is NOT 2,4,6, or 8
 * divisible by 5: yes, last digit is 5 or 0
 * divisible by 10: no, last digit is NOT 0
 * divisible by 3: 3+9+0+7+5=24, yes digits sum to multiple of 3
 * divisible by 6: no, NOT divisible by both 2 and 3

2.4.243)

 * 36/1=36 yes
 * 36/2=18 yes
 * 36/3=13 yes
 * 36/4=9 yes
 * 36/5=7.2 no
 * 36/6=6 yes <-- stop here, quotient is <= divisor

2.4.244)

 * 42/1=42 yes
 * 42/2=21 yes
 * 42/3=14 yes 
 * 42/4=10.5 no
 * 42/5=8.4 no
 * 42/6=7 yes
 * 42/7=6 yes <-- stop here, quotient is <= divisor

2.4.245)

 * 60/1=60 yes
 * 60/2=30 yes
 * 60/3=20 yes
 * 60/4=15 yes
 * 60/5=12 yes
 * 60/6=10 yes
 * 60/7=8.571 no
 * 60/8=7.5 no <-- stop here, quotient is <= divisor

2.4.246)

 * 48/1=48 yes
 * 48/2=24 yes
 * 48/3=16 yes
 * 48/4=12 yes
 * 48/5=9.6 no
 * 48/6=8 yes
 * 48/7=6.857 no <-- stop here, quotient is <= divisor

2.4.247)

 * 144/1=144 yes
 * 144/2=72 yes
 * 144/3=48 yes
 * 144/4=36 yes
 * 144/5=28.8 no
 * 144/6=24 yes
 * 144/7=20.571 no
 * 144/8=18 yes
 * 144/9=16 yes
 * 144/10=14.4 no
 * 144/11=13.090 no
 * 144/12=12 yes <-- stop here, quotient is <= divisor

2.4.248)

 * 200/1=200 yes
 * 200/2=100 yes
 * 200/3=66.666 no
 * 200/4=50 yes
 * 200/5=40 yes
 * 200/6=33.333 no
 * 200/7=28.571 no
 * 200/8=25 yes
 * 200/9=22.222 no
 * 200/10=20 yes
 * 200/11=18.181 no
 * 200/12=16.666 no
 * 200/13=15.384 no
 * 200/14=14.285 no
 * 200/15=13.333 no <-- stop here, quotient is <= divisor

2.4.249)

 * 588/1=588 yes
 * 588/2=294 yes
 * 588/3=196 yes
 * 588/4=147 yes
 * 588/5=117.6 no
 * 588/6=98 yes
 * 588/7=84 yes
 * 588/8=73.5 no
 * 588/9=65.333 no
 * 588/10=58.8 no
 * 588/11=53.4545 no
 * 588/12=49 yes
 * 588/13=45.230 no
 * 588/14=42 yes
 * 588/15=39.2 no
 * 588/16=36.75 no
 * 588/17=34.588 no
 * 588/18=32.666 no
 * 588/19=30.947 no
 * 588/20=29.4 no
 * 588/21=28 yes
 * 588/22=26.727 no
 * 588/23=25.565 no
 * 588/24=24.5 no
 * 588/25=23.52 no

2.4.250)

 * 576/1=576 yes
 * 576/2=288 yes
 * 576/3=192 yes
 * 576/4=144 yes
 * 576/5=115.2 no
 * 576/6=96 yes
 * 576/7=82.285 no
 * 576/8=72 yes
 * 576/9=64 yes
 * 576/10=57.6 no
 * 576/11=52.363 no
 * 576/12=48 yes
 * 576/13=44.307 no
 * 576/14=41.142 no
 * 576/15=38.4 no
 * 576/16=36 yes
 * 576/17=33.882 no
 * 576/18=32 yes
 * 576/19=30.315 no
 * 576/20=28.8 no
 * 576/21=27.428 no
 * 576/22=26.181 no
 * 576/23=25.043 no
 * 576/24=24 yes <-- stop here, quotient is <= divisor

2.4.251)

 * 43/1=43 yes
 * 43/2 no -- fails common divisibility test
 * 43/3 no -- fails common divisibility test
 * 43/4=10.75 no
 * 43/5 no -- fails common divisibility test
 * 43/6 no -- fails common divisibility test
 * 43/7=6.142 no <-- stop here, quotient is <= divisor

43 is prime, its only factors are 1 and itself

2.4.252)

 * 67/1=67 yes
 * 67/2 no -- fails common divisibility test
 * 67/3 no -- fails common divisibility test
 * 67/4=16.75 no
 * 67/5 no -- fails common divisibility test
 * 67/6 no -- fails common divisibility test
 * 67/7=9.571 no
 * 67/8=8.375 no
 * 67/9=7.444 no <-- stop here, quotient is <= divisor

67 is prime, its only factors are 1 and itself

2.4.253)

39 is composite -- it's divisible by 3 (see common divisibility tests), which means it has over 2 factors(1, itself, 3, and maybe more)

2.4.254)

 * 53/1=53 yes
 * 53/2 no -- fails common divisibility test
 * 53/3 no -- fails common divisibility test
 * 53/4=13.25 no
 * 53/5 no -- fails common divisibility test
 * 53/6 no -- fails common divisibility test
 * 53/7=7.571 no
 * 53/8=6.625 no <-- stop here, quotient is <= divisor

53 is prime, its only factors are 1 and itself

2.4.255)

 * 71/1=71
 * 71/2 no -- fails common divisibility test
 * 71/3 no -- fails common divisibility test
 * 53/4=17.75 no
 * 71/5 no -- fails common divisibility test
 * 71/6 no -- fails common divisibility test
 * 71/7=10.142 no
 * 71/8=8.875 no
 * 71/9=7.888 no <-- stop here, quotient is <= divisor

71 is prime, its only factors are 1 and itself

2.4.256)

 * 119/1=119
 * 119/2 no -- fails common divisibility test
 * 119/3 no -- fails common divisibility test
 * 119/4=29.75 no
 * 119/5 no -- fails common divisibility test
 * 119/6 no -- fails common divisibility test
 * 119/7 yes <-- stop her, it's divisible by 7 which means it has over 2 factors(1, itself, 7, and maybe more)

119 is composite

2.4.257)

 * 481/1=481
 * 481/2 no -- fails common divisibility test
 * 481/3 no -- fails common divisibility test
 * 481/4=120.25 no
 * 481/5 no -- fails common divisibility test
 * 481/6 no -- fails common divisibility test
 * 481/7=68.714 no
 * 481/8
 * 481/9=53.444 no
 * 481/10=48.1 no
 * 481/11=43.727 no
 * 481/13=37 <-- stop her, it's divisible by 13 which means it has over 2 factors(1, itself, 13, and maybe more)

481 is composite

2.4.258)

 * 221/1=221
 * 221/2 no -- fails common divisibility test
 * 221/3 no -- fails common divisibility test
 * 221/4=55.25 no
 * 221/5 no -- fails common divisibility test
 * 221/6 no -- fails common divisibility test
 * 221/7=31.571 no
 * 221/8=27.265 no
 * 221/9=24.555 no
 * 221/10=22.1 no
 * 221/11=20.090 no
 * 221/12=18.416 no
 * 221/13=17 <-- stop her, it's divisible by 13 which means it has over 2 factors(1, itself, 13, and maybe more)

221 is composite

2.4.259)

 * 209/1=209
 * 209/2 no -- fails common divisibility test
 * 209/3 no -- fails common divisibility test
 * 209/4=52.25 no
 * 209/5 no -- fails common divisibility test
 * 209/6 no -- fails common divisibility test
 * 209/7=29.857 no
 * 209/8=26.125 no
 * 209/9=23.222 no
 * 209/10=20.9 no
 * 209/11=19 <-- stop her, it's divisible by 11 which means it has over 2 factors(1, itself, 11, and maybe more)

209 is composite

2.4.260)

 * 359/1=359
 * 359/2 no -- fails common divisibility test
 * 359/3 no -- fails common divisibility test
 * 359/4=89.75 no
 * 359/5 no -- fails common divisibility test
 * 359/6 no -- fails common divisibility test
 * 359/7=51.285 no
 * 359/8=44.875
 * 359/9=39.888 no
 * 359/10=35.9 no
 * 359/11=32.636 no
 * 359/12=29.916 no
 * 359/13=27.615 no
 * 359/14=25.642 no
 * 359/15=23.933 no
 * 359/16 no
 * 359/17=21.117 no
 * 359/18 no
 * 359/19 = 18.1784  <-- stop here, quotient is <= divisor

359 is prime

2.4.261)

 * 667/1=667
 * 667/2 no -- fails common divisibility test
 * 667/3 no -- fails common divisibility test
 * 667/4=116.75 no
 * 667/5 no -- fails common divisibility test
 * 667/6 no -- fails common divisibility test
 * 667/7=94.285 no
 * 667/8 no
 * 667/9=74.111 no
 * 667/10=66.7 no
 * 667/11=60.636 no
 * 667/12 no
 * 667/13=51.307 no
 * 667/14 no
 * 667/15 no
 * 667/16 no
 * 667/17=39.235 no
 * 667/18 no
 * 667/19=35.105 no
 * 667/20 no
 * 667/21=31.761 no
 * 667/22 no
 * 667/23=29 <-- stop her, it's divisible by 29 which means it has over 2 factors(1, itself, 29, and maybe more)

2.4.262)

 * 1771/1=1771
 * 1771/2 no -- fails common divisibility test
 * 1771/3 no -- fails common divisibility test
 * 1771/4=442.75 no
 * 1771/5 no -- fails common divisibility test
 * 1771/6 no -- fails common divisibility test
 * 1771/7=253 <-- stop her, it's divisible by 7 which means it has over 2 factors(1, itself, 7, and maybe more)

2.4.263)

 * 200+(15*3)=145
 * 200+(15*4)=160
 * 200+(15*5)=175
 * 200+(15*6)=190
 * 200+(15*20)=500
 * 200+(15\*x)=200+(15\*x)

2.4.264)

 * 75+(20*3)=135
 * 75+(20*4)=155
 * 75+(20*5)=175
 * 75+(20*6)=195
 * 75+(20*20)=475
 * 75+(20\*x)=75+(20\*x)

2.4.265)

6 is a composite of 2 and 3, meaning that 6 has the factors 2 and 3 -- 6=2*3.

Multiplying any number by 6 is the same as multiplying it by 2\*3. For example, 10\*6=60, 10\*2\*3=60. Since you're multiplying by both 2 and 3, the product is divisible by both 2 and 3.

10\*2\*3=60 can be reordered as (10\*2)\*3=60, then simplified to 20\*3=60 -- meaning 60 is divisible by 3

10\*2\*3=60 can be reordered as (10\*3)\*2=60, then simplified to 30\*2=60 -- meaning 60 is divisible by 3

2.4.266)

A prime number has 2 factors -- 1 and itself

A composite number as more than 2 factors -- 1, itself, and others

1 is neither a prime nor a composite since it only has 1 factor: itself.

## Chapter 2 Section 2.5

__TRY IT__

2.95)

START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE
START BACK UP HERE

START BACK UP HERE
START BACK UP HERE
START BACK UP HERE