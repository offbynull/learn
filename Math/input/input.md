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
diagramhelper_code/
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
diagramhelper_code/
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
diagramhelper_code/
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
diagramhelper_code/
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

Common properties of addition:

 * commutative: order in which 2 numbers are added doesn't matter
   
   ```
    [●●●]    [●●●●●] results in [●●●●●●●●]    (3+5 is 7)
      3         5                    7
   
    [●●●●●]   [●●●]  results in [●●●●●●●●]    (5+3 is 7)
      5         3                    7
   ```

 * identity: any number plus 0 results in the same number

   ```
   [●●●]    [] results in [●●●]    (3+0 is 3)
     3       0              3

   []    [●●●] results in [●●●]    (0+3 is 3)
    0      3                3
   ```

## Vertical Addition Algorithm

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
│
└───── ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
```

The digit in the 10s place is the result for the 10s place, while the digit in the 100s place gets combined in with the 100s place. In the above example, the 100s place was empty, so the carry-over remained as-is.

The way to perform this algorithm in real-life is to stack the two numbers being added on top of each other, where the positions for both numbers match up (e.g. the 1s position matches up, the 10s position matches up, the 100s position matched up, etc..). Then, add the individual single digit components together (from right-to-left). For example...

```{define-block}
ktvertadd
ktvertadd_macro/
kthelper_code/
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

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE

TODO: WRITE PLUGIN TO DUMP FILE AS CODE AND DUMP OUT THE CODE HERE



For example, adding 191 to 273...

```{define-block}
wholenumadd
wholenumadd_macro/
wholenum_code/
```

```{wholenumadd}
273 991
```

# Subtraction

TODO: Chapter 1.3

Pay special attention to exercise problem 1.3.204 / 1.3.205 when codifying.

```{define-block}
ktvertsub
ktvertsub_macro/
kthelper_code/
```

```{ktvertsub}
{1}{10}
{2}{0}
{1}{1}
------
{0}{9}
```

KaTeX vertical subtraction template. Wrap digit with \cancel to strike it (e.g. `\cancel{d}`).

```
`{kt}
\begin{alignedat}{4}
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \\
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }&  \enspace - \\
\hline
       {  }&  \enspace        {  }&  \enspace        {  }&  \enspace        {  }& 
\end{alignedat}
`
```

For example...

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

# Multiplication

`{bm} product` is the result of division.

```{define-block}
ktvertmul
ktvertmul_macro/
kthelper_code/
```

```{ktvertmul}
{ }{1}{1}
{ }{1}{0}
-----
{ }{0}{0}
{1}{0}{0}
------
{1}{0}{0}
```


# Division

`{bm} quotient` is the result of division.

`{bm} dividend` is the number being divided.

`{bm} divisor` is the number being divided by.

`{kt} dividend \div divisor = quotient`

`{kt} dividend / divisor = quotient`

`{kt} \frac{dividend}{divisor} = quotient`

`{kt}
\begin{array}{l}
\phantom{
  {divisor\smash{)}}
}{
  quotient
} \\
{divisor}\overline{\smash{)}dividend} \\
\end{array}
`

Why is division by 0 not possible (undefined)?

If you think of division as iterative subtraction, how many times can you remove 0 from a number until it's less than 0? e.g. 24/0. You'll keep subtracting 0s forever (infinity).

If you think of division as the inverse of multiplication... if 10/0=x, then x*0=10 -- but any number multiplied by 0 will still equal zero.

```{define-block}
ktlongdiv
ktlongdiv_macro/
kthelper_code/
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

```
`{kt}
\begin{array}{l}
\phantom{
  {5\smash{)}}
}{
  047.9
} \\
{5}\overline{\smash{)}239.5} \\
\phantom{{5\smash{)}}}\underline{0} \\
\phantom{{5\smash{)}}}23 \\
\phantom{{5\smash{)}}}\underline{20} \\
\phantom{{5\smash{)}}}\phantom{0}39 \\
\phantom{{5\smash{)}}}\phantom{0}\underline{35} \\
\phantom{{5\smash{)}}}\phantom{00}4\phantom{.}5 \\
\phantom{{5\smash{)}}}\phantom{00}\underline{4\phantom{.}5} \\
\phantom{{5\smash{)}}}\phantom{004.}0 \\
\end{array}
`
```

`{kt}
\begin{array}{l}
\phantom{
  {5\smash{)}}
}{
  047.9
} \\
{5}\overline{\smash{)}239.5} \\
\phantom{{5\smash{)}}}\underline{0} \\
\phantom{{5\smash{)}}}23 \\
\phantom{{5\smash{)}}}\underline{20} \\
\phantom{{5\smash{)}}}\phantom{0}39 \\
\phantom{{5\smash{)}}}\phantom{0}\underline{35} \\
\phantom{{5\smash{)}}}\phantom{00}4\phantom{.}5 \\
\phantom{{5\smash{)}}}\phantom{00}\underline{4\phantom{.}5} \\
\phantom{{5\smash{)}}}\phantom{004.}0 \\
\end{array}
`

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