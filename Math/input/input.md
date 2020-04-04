```{define-block}
svgbob
svgbob_macro/
```

```{define-block}
prereq
prereq_macro/
prereq_code/
```

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

## Naming

TODO: Discuss number to word transitions (2nd part of Chapter 1.1)

21,055 is the same as saying twenty one thousand fifty five

# Arithmetic

TODO: discuss arithmetic -- it's the study of numbers and the traditional operations on them: addition, subtraction, multiplication and division

## Addition

```{prereq}
Place value system
```

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

## Subtraction

```{prereq}
Place value system
```

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

## Multiplication

```{prereq}
Place value system
Addition
```

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

## Division

```{prereq}
Place value system
Subtraction
```

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

# Whole Number

```{prereq}
Place-value system
```

```{svgbob}
+-+------------------------------+ 
| |                              | 
| |   "Natural (e.g. 1, 7, 291)" | 
| |                              | 
| +------------------------------+ 
|                                | 
|   "Whole (0)"                  | 
|                                | 
+--------------------------------+ 
```

`{bm} Whole number`s are numbers which have no partial portion -- they only consist of wholes. For example, 5, 0, 104, and 27 are whole numbers while 4.2 is not.

```{svgbob}
+-+-+-+-+-+-+-+-+-->
| | | | | | | | | 
0 1 2 3 4 5 6 7 8
```

The difference between whole numbers and `{bm} natural \/ counting \/ cardnial number/(natural number|counting number|cardinal number)/i`s is that counting numbers don't include 0 (they start at 1). That is, counting numbers start where you start counting / where something exists. For example, if you're counting apples, you start counting at 1 -- there needs to be at least 1 apple to start.

## Addition

```{prereq}
Addition
```

`{bm} /(whole number addition|add whole numbers|addition of whole numbers)/i`

The algorithm used by humans to add large whole numbers together is called `{bm} vertical addition`. Vertical addition relies on two ideas...

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
arithmetic_code/WholeNumber.py
python
#MARKDOWN_ADD\s*\n([\s\S]+)\n\s*#MARKDOWN_ADD
```

```{define-block}
wholenumadd
wholenumadd_macro/
arithmetic_code/
```

```{wholenumadd}
273 991
```

## Subtraction

```{prereq}
Subtraction
```

`{bm} /(whole number subtraction|subtract whole numbers)/i`

The algorithm used by humans to subtract large whole numbers from each other is called `{bm} vertical subtraction`. Vertical subtraction relies on two ideas...

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
arithmetic_code/WholeNumber.py
python
#MARKDOWN_SUB\s*\n([\s\S]+)\n\s*#MARKDOWN_SUB
```

```{define-block}
wholenumsub
wholenumsub_macro/
arithmetic_code/
```

```{wholenumsub}
100 11
```

## Multiplication

```{prereq}
Multiplication
Whole number addition
```

`{bm} /(whole number multiplication|multiply whole numbers)/i`

The algorithm used by humans to multiply large whole numbers together is called `{bm} vertical multiplication`. Vertical multiplication relies on three ideas...

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
arithmetic_code/WholeNumber.py
python
#MARKDOWN_MUL\s*\n([\s\S]+)\n\s*#MARKDOWN_MUL
```

```{define-block}
wholenummul
wholenummul_macro/
arithmetic_code/
```

```{wholenummul}
77 87
```

## Division

```{prereq}
Division
```

`{bm} /(whole number division|divide whole numbers)/i`

There are 2 algorithms used to divide large whole numbers:

 * trial-and-error division
 * long division (requires trial-and-error division)

These algorithms are detailed in the subsections below.

### Trial and Error

```{prereq}
Whole number subtraction
Whole number multiplication
```

`{bm} Trial-and-error division` is an algorithm used for dividing numbers. The core idea behind the algorithm is that multiplication is the inverse of division. That is, multiplication reverses / un-does division (and vice-versa). For example...

* 3 * 4 is 12 -- If you have 3 groups of 4 items each, you'll have 12 items.
* 12 / 3 is 4 -- If you have 12 items and you break them up into 3 groups, you'll have 4 items in each group.

```{svgbob}
"3 * 4 is 12"       "12 / 3 is 4"
          
  +----+          +----+----+----+
  |●●●●| 4        |●●●●|●●●●|●●●●| 12
  +----+          +----+----+----+
  |●●●●| 4          4    4    4  
  +----+  
  |●●●●| 4
  +----+  
    12    



        +------------+
        |            |
        |  +--+     +++    +-+
        |  |12| "/" |3| is |4|---+
        |  +-++     +-+    +-+   |
        |    |                   |
        |    +-------------+     |
        |                  |     |
        |                  v     |
        |  +-+     +-+    +--+   |
        +->|3| "*" |4| is |12|   |
           +-+     +-+    +--+   |
                    ^            |
                    |            |
                    +------------+
```

Knowing this, multiplication can be used to check if some number is the quotient. For example, to find the quotient for 20 / 5...

```{svgbob}
+------------+
|            |
|  +--+     +++    +-+
|  |20| "/" |5| is |?+---+
|  +-++     +-+    +-+   |
|    |                   |
|    +-------------+     |
|                  |     |
|                  v     |
|  +-+     +-+    +--+   |
+->|5| "*" |?| is |20|   |
   +-+     +++    +--+   |
            ^            |
            |            |
            +------------+
```

* 5 * 1 is 5 <-- test 1, no
* 5 * 2 is 10 <-- test 2, no
* 5 * 3 is 15 <-- test 3, no
* 5 * 4 is 20 <-- test 4, FOUND -- 20 / 5 is 4

5 * 4 is 20 -- If you have 5 groups of 4 items each, you'll have 20 items.

```{svgbob}
"5 * 4 is 20"         "20 / 5 is 4"

  +----+       +----+----+----+----+----+
  |●●●●| 4     |●●●●|●●●●|●●●●|●●●●|●●●●| 20
  +----+       +----+----+----+----+----+
  |●●●●| 4       4    4    4    4    4   
  +----+  
  |●●●●| 4
  +----+  
  |●●●●| 4
  +----+  
  |●●●●| 4
  +----+  
    20    



        +------------+
        |            |
        |  +--+     +++    +-+
        |  |20| "/" |5| is |4|---+
        |  +-++     +-+    +-+   |
        |    |                   |
        |    +-------------+     |
        |                  |     |
        |                  v     |
        |  +-+     +-+    +--+   |
        +->|5| "*" |4| is |20|   |
           +-+     +++    +--+   |
                    ^            |
                    |            |
                    +------------+
```

Rather than testing each number one-by-one, it's faster to start with a number range and narrow / tweak it until you converge to the answer. That is, start with an arbitrary lower-bound and upper-bound and test both. If the product is...

* within the bound, narrow the number range by some amount.
* above the bound, move the range down.
* below the bound, move the range up.

Repeat until the answer is found.

For example, 2617 / 52...

```{svgbob}
+--------------+
|              |
|  +----+     ++-+    +-+
|  |2617| "/" |52| is |?+---+
|  +-+--+     +--+    +-+   |
|    |                      |
|    +---------------+      |
|                    |      |
|                    v      |
|  +--+     +-+    +----+   |
+->|52| "*" |?| is |2617|   |
   +--+     +++    +----+   |
             ^              |
             |              |
             +--------------+
```

Decide on a range and test...

* ? = [10, 100]
  * 10 * 52 = 520
  * 100 * 52 = 5200

2617 sits BETWEEN the range, so narrow...

* ? = [20, 40]
  * 20 * 52 = 1040
  * 40 * 52 = 2080

2617 sits BELOW the range, so move up...

* ? = [40, 60]
  * 40 * 52 = 2080
  * 60 * 52 = 3120

2617 sits between the range, so narrow...

* ? = [50, 51]
  * 50 * 52 = 2600
  * 51 * 52 = 2652

2617 sits between the range but doesn't make sense to narrow any further. The quotient is 50, the remainder is 17 (2617 - 2600).

```{note}
There's a specific algorithm for picking a starting range as well as how much to tweak that range in each iteration. You'll find those algorithms if you view the file for the code below (they aren't shown in the output).

If you're doing this on paper you can just look and guess. If you're writing code you should probably use these algorithms or come up with something better.
```

The trial-and-error division algorithm written as code is as follows:

```{output}
arithmetic_code/WholeNumber.py
python
#MARKDOWN_DIVTE\s*\n([\s\S]+)\n\s*#MARKDOWN_DIVTE
```

```{define-block}
wholenumdivte
wholenumdivte_macro/
arithmetic_code/
```

```{wholenumdivte}
98 3
```

### Long Division

```{prereq}
Trial-and-error division
Whole number subtraction
```

The algorithm used by humans to divide large whole numbers is called `{bm} long division`. In most cases, it can divide a number in less steps than trial-and-error division. Long division relies on three ideas...

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

2. Any number can be divided using trial-and-error division. For example, 20 / 5...

   ```{svgbob}
   +----------+
   |          |
   |  +--+   +++    +-+
   |  |20| / |5| is |?+---+
   |  +-++   +-+    +-+   |
   |    |                 |
   |    +-----------+     |
   |                |     |
   |                v     |
   |  +-+   +-+    +--+   |
   +->|5| x |?| is |20|   |
      +-+   +++    +--+   |
             ^            |
             |            |
             +------------+
   ```

   * 5 * 1 is 5 <-- test 1, no
   * 5 * 9 is 45 <-- test 9, no
   * 5 * 2 is 10 <-- test 2, no
   * 5 * 8 is 40 <-- test 8, no
   * 5 * 3 is 15 <-- test 3, no
   * 5 * 7 is 35 <-- test 7, no
   * 5 * 4 is 20 <-- test 4, FOUND -- 20 / 5 is 4

3. When dividing, if the number being divided (dividend) has trailing zeros, those trailing zeros can be removed prior to the division and then put back on after the division. For example, 4500 / 6...

   ```{svgbob}
            remove trailing 0s from dividend
        +-----------------------------------------+
        |                                         |
        |                                         v
   +--+-++     +-+                              +--+
   |45|00| "/" |6|                              |00|
   ++-+--+     +++                              +-++
    |           |                                 |
    |        +--+                                 |
    |        |                                    |
    v        v                                    |
   +--+     +-+                                   |
   |45| "/" |6|                                   |
   +-++     +++                                   |
     |       |                                    |
     v       v                                    |
   +-----------------+                            |
   | trial and error |                            |
   |     division    |                            |
   +--+---+----------+                            |
      |   |                                       |
      v   v                                       |
     +-+ +-+                                      |
     |7|R|3|                                      |
     +++ +++                                      |
      |   |                                       |
    +-+   ++                                      |
    |      |                                      |
    v      v                                      |
   +-+--+ +-+--+                                  |
   |7|00|R|3|00|                                  |
   +-+--+ +-+--+                                  |
       ^      ^                                   |
       |      |                                   |
       |      +-----------------------------------+
       |                                          |
       +------------------------------------------+
            append trailing 0s to answer
   ```

   When 4500 items are broken up into groups of 6, this rule says that there will be _at least_ 700 groups. 300 of the 4500 items remain unaccounted for, but the rule can be used again on these 300 items because 300 has trailing 0s (recursive).

   ```{note}
   It's easy to test if this is correct... 
   * 700 \* 6 = 4200    (multiply by the quotient)
   * 4200 + 300 = 4500  (add the remainder)
   ```

   ```{note}
   The reasoning behind why trailing 0s can be removed and re-appended has to do with expressions / order of operations / factoring. Taking the original 4500 / 7 example above...
   
    * 4500 / 7
    * (45 * 100) / 7  <-- factor out 100 from the 4500
    * 45 * 100 / 7 <-- remove parenthesis, associativity law, mult and div have same precedence so it doesn't matter which gets performed first
    * 45 / 7 * 100 <-- swap, commutative law, mult and div have same precedence so it doesn't matter which gets performed first
    * (45 / 7) * 100
    * (7R3) * 100
    * 700R300
   ```

   In certain cases, the quotient returned by the operation will end up being 0. This means that the operation failed.
   
   If this happens, less trialing-zeros need to be stripped-off. Keep leaving in trialing 0s and re-doing the operation until the quotient becomes non-zero. For example, when all 3 trailing 0s are stripped from 4000 / 6...

   ```{svgbob}
            remove trailing 0s from dividend
        +-----------------------------------------+
        |                                         |
        |                                         v
   +-+--++     +-+                              +---+
   |4|000| "/" |6|                              |000|
   +++---+     +++                              +-+-+
    |           |                                 |
    |       +---+                                 |
    |       |                                     |
    v       v                                     |
   +-+     +-+                                    |
   |4| "/" |6|                                    |
   +++     +++                                    |
    |       |                                     |
    v       v                                     |
   +-----------------+                            |
   | trial-and-error |                            |
   |     division    |                            |
   +--+---+----------+                            |
      |   |                                       |
      v   v                                       |
     +-+ +-+                                      |
     |0|R|4|                                      |
     +++ +++                                      |
      |   |                                       |
    +-+   +-+                                     |
    |       |                                     |
    v       v                                     |
   +-+---+ +-+---+                                |
   |0|000|R|4|000|                                |
   +-+---+ +-+---+                                |
       ^       ^                                  |
       |       |                                  |
       |       +----------------------------------+
       |                                          |
       +------------------------------------------+
            append trailing 0s to answer
   ```

   ... the quotient is 0 and the remainder is 4000. The operation pretty much failed because the amount of remaining items is the same as the amount starting amount -- nothing was grouped and everything remains. As such, more trialing 0s need to be left in. Re-try the operation with only 2 trialing 0s removed... 

   ```{svgbob}
            remove trailing 0s from dividend
        +-----------------------------------------+
        |                                         |
        |                                         v
   +--+-++     +-+                              +--+
   |40|00| "/" |6|                              |00|
   ++-+--+     +++                              +-++
    |           |                                 |
    |        +--+                                 |
    |        |                                    |
    v        v                                    |
   +--+     +-+                                   |
   |40| "/" |6|                                   |
   +-++     +++                                   |
     |       |                                    |
     v       v                                    |
   +-----------------+                            |
   | trial-and-error |                            |
   |     division    |                            |
   +--+---+----------+                            |
      |   |                                       |
      v   v                                       |
     +-+ +-+                                      |
     |6|R|4|                                      |
     +++ +++                                      |
      |   |                                       |
    +-+   ++                                      |
    |      |                                      |
    v      v                                      |
   +-+--+ +-+--+                                  |
   |6|00|R|4|00|                                  |
   +-+--+ +-+--+                                  |
       ^      ^                                   |
       |      |                                   |
       |      +-----------------------------------+
       |                                          |
       +------------------------------------------+
            append trailing 0s to answer
   ```

   ... the quotient is 600 and the remainder is 400.  When 4000 items are broken up into groups of 6, there will be _at least_ 600 groups. 400 of the 4000 items remain unaccounted for, but the rule can be used again on these 400 items because 400 has trailing 0s (recursive).

The idea behind long division is to break up the dividend into its individual single digit components results (idea 1) and divide each component by the divisor. For example, 752 / 3...

```{svgbob}
                              752               
                               |                    
                               v                    
                           +-------+                
       +-------------------+ BREAK +---------------+
       |                   +---+---+               |
       |                       |                   |
       v                       v                   v
      700                     50                   2
       |                       |                   |
       |                       |                   |
       v                       v                   v
 how many groups        how many groups     how many groups
 of 3 does 700          of 3 does 50        of 2 does 3
 make? "700 / 3"        make? "50 / 3"      make? "2 / 3"
```

Each of the divisions are easy to perform because trialing 0s can be stripped-off prior to trial-and-error division (ideas 2 and 3). That is, the actual numbers being input into trial-and-error division are much smaller than they would normally be because trailing 0s are removed. Smaller numbers mean easier to perform.

```{svgbob}
                              752                 
                               |                    
                               v                    
                           +-------+                
       +-------------------+ BREAK +---------------+
       |                   +---+---+               |
       |                       |                   |
       v                       v                   v
      700                     50                   2
       |                       |                   |
       v                       v                   v
     +--+                    +--+                +--+   
   +-|TE|-+                +-|TE|-+            +-|TE|-+ 
   | +--+ |                | +--+ |            | +--+ | 
   v      v                v      v            v      v 
  200    R100             10     R20           0      R2
                  
  at least 200            at least 10          at least 0   
  groups of 3             groups of 3          groups of 3   
  with 100 items          with 20 items        with 2 items
  unaccounted             unaccounted          unaccounted   
  for                     for                  for            
```

```{note}
The TE block is applying idea 3. The trialing 0s are being stripped off, trial-and-error division is being performed, then the 0s are re-append to the quotient and the remainder.
```

The remainders need to be accounted for. That is, if there are enough remaining items to form a group, they should be grouped. The process is repeated on the remaining items until there aren't enough to form a group (until the remainder is less than the divisor). Once there aren't enough remaining items to form a group, the sum of the quotients becomes the final quotient (final number of groups) and the remainder becomes the final remainder...

```{note}
The diagram below looks daunting but it's just 3 copies of the diagrams above stacked on top of each other -- 1 for each iteration. The remainders from each iteration are being combined and used as the input for the next iteration. The quotients from each iteration are being combined to get the total quotient (total number of groups).

The diagram is intended to be an intermediary step to reasoning about long division. There's further simplification / explanation after it.
```


```{svgbob}
                              752 (ITERATION 1)                 
                               |                    
                               v                    
                           +-------+                
       +-------------------+ BREAK +---------------+
       |                   +---+---+               |
       |                       |                   |
       v                       v                   v
      700                     50                   2
       |                       |                   |
       v                       v                   v
     +--+                    +--+                +--+   
   +-|TE|-+                +-|TE|-+            +-|TE|-+ 
   | +--+ |                | +--+ |            | +--+ | 
   v      v                v      v            v      v 
  200    R100             10     R20           0      R2
   |      |                |      |             |      \            +-+
   |      |                |      \             +-------]---------->|A|
   |      \                +-------]--------------------]---------->|D|
   +-------]-----------------------]--------------------]---------->|D|
          /                       /                    /            +++ 
          |                       |                    |             |
          +--------------------+--+--------------------+             v
                               |                                    210
                               v                                     |
                             +---+                                   |
                             |ADD|                                   |
                             +-+-+                                   |
                               |                                     |
                               v                                     |
                              122 (ITERATION 2)                      |
                               |                                     |
                               |                                     |
                               v                                     |
                           +-------+                                 |
       +-------------------+ BREAK +---------------+                 |
       |                   +---+---+               |                 |
       |                       |                   |                 |
       v                       v                   v                 |
      100                     20                   2                 |
       |                       |                   |                 |
       v                       v                   v                 |
     +--+                    +--+                +--+                |
   +-|TE|-+                +-|TE|-+            +-|TE|-+              |
   | +--+ |                | +--+ |            | +--+ |              |
   v      v                v      v            v      v              |
  30     R10               6      R2           0      R2             v
   |      |                |      |            |       \            +-+
   |      |                |      \            +--------]---------->|A|
   |      \                +-------]--------------------]---------->|D|
   +-------]-----------------------]--------------------]---------->|D|
          /                       /                    /            +++ 
          |                       |                    |             |
          +--------------------+--+--------------------+             v
                               |                                    246
                               v                                     |
                             +---+                                   |
                             |ADD|                                   |
                             +-+-+                                   |
                               |                                     |
                               v                                     |
                               14 (ITERATION 3)                      |
                               |                                     |
                               v                                     |
                           +-------+                                 |
                           | BREAK +---------------+                 |
                           +---+---+               |                 |
                               |                   |                 |
                               v                   v                 |
                              10                   4                 |
                               |                   |                 |
                               v                   v                 |
                             +--+                +--+                |
                           +-|TE|-+            +-|TE|-+              |
                           | +--+ |            | +--+ |              |
                           v      v            v      v              |
                           3     R1            1      R1             v
                           |     |             |      \             +-+
                           |     \             +-------]----------->|A|
                           +------]--------------------]----------->|D|
                                 /                    /             |D|
                                 |                    |             +++ 
                                 |                    |              |
                                 +--------------------+              |
                                 |                                   |
                                 v                                   |
                               +---+                                 |
                               |ADD|                                 |
                               +-+-+                                 |
                                 |                                   |
                                 v                                   v
                                 2                                  250
                          (final remainder)                   (final quotient)
```

The answer to 752 / 3 is 250R2.

```{note}
You can confirm this by doing 250 * 3 then adding 2. The result should be 752.
```

This process can be made much simpler by focusing on one component at a time. Starting from the largest component to the smallest component, divide (using idea 3) but then roll-in (add) the remainder into the next component. The thought process is exactly the same as above -- the division is being performed on a component and the remaining items from that division are being accounted for because they're being added to the next component (which gets divided next). For example, 752 / 3...

```{note}
Notice how the inputs to TE still have trailing 0s.
```

 1. Divide the largest component (700)...

    ```{svgbob}
                                  752                 
                                   |                    
                                   v                    
                               +-------+                
           +-------------------+ BREAK +---------------+
           |                   +---+---+               |
           |                       |                   |
           v                       v                   v
          700                     50                   2
           |      
           v      
         +--+     
       +-|TE|-+   
       | +--+ |   
       v      v   
      200    R100 
    ```

 2. Roll in remainder to the second largest component (50) and divide...

    ```{svgbob}
                                  752                 
                                   |                    
                                   v                    
                               +-------+                
           +-------------------+ BREAK +---------------+
           |                   +---+---+               |
           |                       |                   |
           v                       v                   v
          700                     50                   2
           |                       |    
           v                       |    
         +--+                      |    
       +-|TE|-+                    |    
       | +--+ |                    |    
       v      v                    |    
      200    R100                  v    
              |                  +---+  
              +----------------->|ADD|  
                                 +---+  
                                   |    
                                   v    
                                  150   
                                   |    
                                   v    
                                 +--+   
                               +-|TE|-+ 
                               | +--+ | 
                               v      v 
                              50     R00
    ```

 3. Roll in remainder to the third largest component (2) and divide...

    ```{svgbob}
                                  752                 
                                   |                    
                                   v                    
                               +-------+                
           +-------------------+ BREAK +---------------+
           |                   +---+---+               |
           |                       |                   |
           v                       v                   v
          700                     50                   2
           |                       |                   |
           v                       |                   |
         +--+                      |                   |
       +-|TE|-+                    |                   |
       | +--+ |                    |                   |
       v      v                    |                   |
      200    R100                  v                   |
              |                  +---+                 |
              +----------------->|ADD|                 |
                                 +---+                 |
                                   |                   |
                                   v                   |
                                  150                  |
                                   |                   |
                                   v                   |
                                 +--+                  |
                               +-|TE|-+                |
                               | +--+ |                |
                               v      v                |
                              50     R00               v
                                      |              +---+
                                      +------------->|ADD|
                                                     +---+
                                                       |
                                                       v
                                                       2
                                                       |     
                                                       v     
                                                     +--+    
                                                   +-|TE|-+  
                                                   | +--+ |  
                                                   v      v  
                                                   0     R2
    ```

 4. The sum of the quotients becomes the final quotient, and the last remainder becomes the final remainder...

    ```{svgbob}
                                  752                 
                                   |                    
                                   v                    
                               +-------+                
           +-------------------+ BREAK +---------------+
           |                   +---+---+               |
           |                       |                   |
           v                       v                   v
          700                     50                   2
           |                       |                   |
           v                       |                   |
         +--+                      |                   |
       +-|TE|-+                    |                   |
       | +--+ |                    |                   |
       v      v                    |                   |
      200    R100                  v                   |
       |      |                  +---+                 |
       |      +----------------->|ADD|                 |
       |                         +---+                 |
       |                           |                   |
       |                           v                   |
       |                          150                  |
       |                           |                   |
       |                           v                   |
       |                         +--+                  |
       |                       +-|TE|-+                |
       |                       | +--+ |                |
       |                       v      v                |
       |                      50     R00               v
       |                       |      |              +---+
       |                       |      +------------->|ADD|
       |                       |                     +---+
       |                       |                       |
       |                       |                       v
       |                       |                       2
       |                       |                       |     
       |                       |                       v     
       |                       |                     +--+    
       |                       |                   +-|TE|-+  
       |                       |                   | +--+ |  
       |                       |                   v      v  
       |                       |                   0     R2
       |                       |                   |      |
       +----------+------------+-------------------+      |
                  |                                       |
                  v                                       |
                +---+                                     |
                |ADD|                                     |
                +---+                                     |
                  |                                       |
                  v                                       v
                 250                                     R2
            (final quotient)                     (final remainder)
    ```

This is effectively the algorithm that humans use for long division -- for each component, divide (using idea 3) and roll in the remainder to the next component. Repeat the process until there are no components remaining.

The notation used by humans for long division is...

```{define-block}
ktlongdiv
ktlongdiv_macro/
kthelper_code/target/appassembler/
```

```{ktlongdiv}
{quotient}
{divisor}{dividend}
```

For example, long division notation for 752 / 3 is initially written as...

```{ktlongdiv}
   {}
{3}{752}
```



Starting with the first component, divide (using idea 3) to get the quotient and remainder for that component: 200R100. Then, strip-off the trialing 0s and place the quotient on-top of the component and the remainder below the component...

```{ktlongdiv}
   {\green{2}}
{3}{752}
   {?}
   {\green{1}}
```

A question mark is sandwiched between the component and remainder. The question mark should be set to the value of the divisor (3) multiplied by the quotient (200), with its trailing 0s stripped out. 3 \* 200 = 600, strip the trialing 0s to get 6...

```{ktlongdiv}
   {2}
{3}{752}
   {\underline{\green{6}}}
   {1}
```

````{note}
The traditional way this is stated when being taught in school is "how many times can 7 go into 3?". Essentially, find the minimum number that the quotient can be without exceeding the component.

* 3\*0 = 0
* 3\*1 = 3
* 3\*2 = 6
* 3\*3 = 9 <-- too large, must be 7 or less, so pick the last one

```{ktlongdiv}
   {2}
{3}{752}
```

Put the answer to 3\*2 = 6 underneath the component, then subtract to get the remainder...

```{ktlongdiv}
   {2}
{3}{752}
   {\underline{6}}
   {1}
```
````

Copy the next largest component down such that it's next the remainder...

```{ktlongdiv}
   {2}
{3}{752}
   {\underline{6}}
   {1\green{5}}
```

This is effectively the same as adding the remainder to the next component: 100 + 50 = 150. Trailing 0s aren't seen because they're implied in long division notation.

````{note}
The traditional way this is stated when being taught in school is "drag down the next component".
````



Repeat the process but target the 15 at the bottom. The 15 is the next component rolled into the remainder...

```{ktlongdiv}
   {2\green{5}}
{3}{752}
   {\underline{6}}
   {15}
   {\underline{\green{15}}}
   {\phantom{0}\green{0}}
```

Copy the next largest component down such that it's next the remainder...

```{ktlongdiv}
   {25}
{3}{752}
   {6}
   {15}
   {15}
   {\phantom{0}0\green{2}}
```



Repeat the entire process but target the 2 at the bottom. The 2 is the next component rolled into the remainder...

```{ktlongdiv}
   {25\green{0}}
{3}{752}
   {\underline{6}}
   {15}
   {\underline{15}}
   {\phantom{0}02}
   {\phantom{00}\underline{\green{0}}}
   {\phantom{00}\green{2}}
```


The final reminder isn't 0, so place it next to the final quotient...

```{ktlongdiv}
   {250\green{R2}}
{3}{752}
   {\underline{6}}
   {15}
   {\underline{15}}
   {\phantom{0}02}
   {\phantom{00}\underline{0}}
   {\phantom{00}2}
```

The way to perform this algorithm via code is as follows...

```{output}
arithmetic_code/WholeNumber.py
python
#MARKDOWN_DIV\s*\n([\s\S]+?)\n\s*#MARKDOWN_DIV
```

```{define-block}
wholenumdiv
wholenumdiv_macro/
arithmetic_code/
```

```{wholenumdiv}
752 3
```

# Integer Number

```{prereq}
Whole numbers
```

```{svgbob}
+-+-+------------------------------+
| | |                              |
| | |   "Natural (e.g. 1, 7, 291)" |
| | |                              |
| | +------------------------------+
| |                                |
| |   "Whole (0)"                  |
| |                                |
| +--------------------------------+
|                                  |
|   "Integer (e.g. -7, -19, -471)" |
|                                  |
+----------------------------------+
```

`{bm} Integer number/(integer number|integer)/i`s are place-value notation numbers that have no partial portion but are mirrored across 0. That is, think of integers as 2 sets of counting numbers separated by 0, where everything to the...

* right of 0 is called a `{bm} positive` number (signified by a + prefix)
* left of 0 is called a `{bm} negative` number (signified by a - prefix)

```{svgbob}
<--+----+----+----+----+----+----+----+----+-->
   |    |    |    |    |    |    |    |    | 
  -4   -3   -2   -1    0   +1   +2   +3   +4
```

The prefix that determines if a integer is positive or negative is referred to as the `{bm} sign`. All numbers other than 0 have a sign. 0 represents nothing / no value, which is why it doesn't have a sign -- it's used as a separation point between the positive and negative values.

```{note}
If a number (other than 0) is positive, the + sign is typically left out. So, ... 
* -5 is -5
+ +5 is +5
* 5 is +5
* 0 is 0
* there is no such thing as -0 (0 never has a sign).
* there is no such thing as +0 (0 never has a sign).
```

Conceptually, you can think of the positives the same way you think about natural numbers. They represent some value. For each positive, there's a corresponding negative that represents the opposite of that positive value. For example, if...

* positive integers represent steps forward, then negative integers would represent steps backward.

  * walk 5 steps (go forward 5 steps)
  * walk -5 steps (go backward 5 steps)

  ```{svgbob}
  <--+-------------------------+-------------------------+-->
     |                         |                         | 
    -5                         0                        +5
  5 feet backward         no movement         5 feet forward
  ```

* positive integers represent money gained, then negative integers would represent money owed or spent.

  * 5 dollars (gain $5)
  * -5 dollars (spend $5, or be in debt $5)

  ```{svgbob}
  <--+-------------------------+-------------------------+-->
     |                         |                         | 
    -5                         0                        +5
  5 dollar debt              broke           5 dollars gained
  ```

* positive integers represent depth below sea-level, then negative integers would represent elevation above sea-level.

  * depth of 5 meters (5 meters below sea-level)
  * depth of -5 meters (5 meters above sea-level)


  ```{svgbob}
  ^
  |
  +- -5 meters deep (5 meters above sea-level)
  |
  |
  |
  +- 0, sea-level
  |
  |
  |
  +- 5 meters deep (5 meters below sea-level)
  |
  v
  ```

## Addition

```{prereq}
Whole number addition
Whole number subtraction
```

Conceptually, you can think of `{bm} integer addition/(integer number addition|integer addition|add integer numbers|add integers|addition of integer numbers|addition of integers)/i` as movement on a number line. If some integer is being added to a...

* positive integer, it's moving right on the number line.

  For example, 3 + 4 is 7...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0 +1 +2 +3 +4 +5 +6 +7 +8
                                      |           ^
                                      |           |
                                      +-----------+
                                            +4
  ```

  For example, -5 + 4 is -1...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0 +1 +2 +3 +4 +5 +6 +7 +8
              |           ^
              |           |
              +-----------+
                    +4
  ```

  Notice that the result of this example's movement is exactly the same as subtracting magnitudes, then tacking on a negative sign to the result: 5 - 4 is 1, tack on a negative sign to get -1.

* negative integer, it's moving left on the number line.

  For example, -1 + -4 is -5...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
              ^           |
              |           |
              +-----------+
                   -4
  ```

  Notice that the result of this example's movement is exactly the same as adding magnitudes, then tacking on a negative sign to the result: 1 + 4 is 5, tack on a negative sign to get -5.

  For example, 3 + -4 is -1...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
                          ^           |
                          |           |
                          +-----------+
                               -4
  ```

  Notice that the result of this example's movement is exactly the same as swapping, subtracting, then tacking on a negative sign to the result: 4 - 3 is 1, tack on a negative sign: -1.

The algorithm used by humans to add integer numbers together revolves around inspecting the sign and magnitude of each integer, then deciding whether to perform whole number addition or whole number subtraction to get the result. The codification of this algorithm is as follows...

```{output}
arithmetic_code/IntegerNumber.py
python
#MARKDOWN_ADD\s*\n([\s\S]+?)\n\s*#MARKDOWN_ADD
```

```{define-block}
intnumadd
intnumadd_macro/
arithmetic_code/
```

```{intnumadd}
-752 3
```

## Subtraction

```{prereq}
Whole number addition
Whole number subtraction
Integer addition
```

Conceptually, you can think of `{bm} integer subtraction/(integer number subtraction|integer subtraction|subtract integer numbers|subtract integers|subtraction of integer numbers|subtraction of integers)/i` as movement on a number line (opposite movement to that of integer addition). If the integer being subtracted by (right-hand side) is a...

* positive integer, it's moving left on the number line.

  For example, 5 - 4 is 1...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0 +1 +2 +3 +4 +5 +6 +7 +8
                                ^           |
                                |           |
                                +-----------+
                                      -4
  ```

  For example, -2 - 4 is -6...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0 +1 +2 +3 +4 +5 +6 +7 +8
           ^           |
           |           |
           +-----------+
                 -4
  ```

  Notice that the result of this example's movement is exactly the same as adding magnitudes, then tacking on a negative sign to the result: 2 + 4 is 6, tack on a negative sign to get -6.

  For example, 3 - 4 is -1...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0 +1 +2 +3 +4 +5 +6 +7 +8
                          ^           |
                          |           |
                          +-----------+
                               -4
  ```

  Notice that the result of this example's movement is exactly the same as swapping, subtracting, then tacking on a negative sign: 4 - 3 is 1, tack on a negative sign to get -1.

* negative integer, it's moving right on the number line.

  For example, 3 - -4 is 7...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
                                      |           ^
                                      |           |
                                      +-----------+
                                            +4
  ```

  Notice that the result of this movement is exactly the same as performing 3 + 4.

  For example, -3 - -4 is 1...

  ```{svgbob}
  <--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+-->
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
                    |           ^
                    |           |
                    +-----------+
                          +4
  ```

  Notice that the result of this example's movement is exactly the same as swapping, subtracting, then tacking on a positive sign to the result: 4 - 3 is 1, tack on a positive sign: 1.

The algorithm used by humans to subtract integer numbers revolves around inspecting the sign and magnitude of each integer, then deciding whether to perform whole number addition or whole number subtraction to get the result. The codification of this algorithm is as follows...

```{output}
arithmetic_code/IntegerNumber.py
python
#MARKDOWN_SUB\s*\n([\s\S]+?)\n\s*#MARKDOWN_SUB
```

```{define-block}
intnumsub
intnumsub_macro/
arithmetic_code/
```

```{intnumsub}
752 -3 
```

## Multiplication

```{prereq}
Whole number multiplication
Integer addition
Integer subtraction
```

Conceptually, you can think of `{bm} integer multiplication/(integer number multiplication|multiply integer numbers|multiply integers|multiplication of integer numbers|multiplication of integers)/i` as repetitive integer addition / integer subtraction. When the right hand side is negative, think of it as subtraction instead of addition. For example, think of ...

* 5 \* 3 as add 5, 3 times

* -5 \* 3 as add -5, 3 times

* 3 \* -5 as subtract 5, 3 times

  ```{note}
  Subtraction starts from 0, so it'd be...
  1. 0 - 5 is -5
  2. -5 - 5 is -10
  3. -10 - 5 is -15

  Or, you could use the commutative property of multiplication and swap the operands -- 3 \* -5 becomes -5 \* 3, exactly the same as the previous bullet point.
  ```

* -5 \* -3 as subtract -5, 3 times

  ```{note}
  Subtraction starts from 0, so it'd be...
  1. 0 - -5 is 5
  2. -5 - -5 is 10
  3. -10 - -5 is 15
  ```

One useful property of integer multiplication is that, multiplying any non-zero number by -1 will slip its sign. For example...

* 5 \* -1 is -5

  1. 0 - 5 is -5

* -5 \* -1 is 5

  1. 0 - -5 is 5

The algorithms humans use to perform integer multiplication is as follows:

1. Ignoring the sign and multiply the numbers using whole number multiplication.
1. If the signs are...
   1. the same, make the result a positive.
   1. different, make the result a negative.

The result produced using the algorithm will be exactly the same as the result produced using repetitive addition/subtraction.

The way to perform this algorithm via code is as follows...

```{output}
arithmetic_code/IntegerNumber.py
python
#MARKDOWN_MUL\s*\n([\s\S]+?)\n\s*#MARKDOWN_MUL
```

```{define-block}
intnummul
intnummul_macro/
arithmetic_code/
```

```{intnummul}
-6 -5
```

## Division

```{prereq}
Whole number division
Integer subtraction
Integer addition
Integer multiplication
```

Conceptually, you can think of `{bm} integer division/(integer number division|divide integer numbers|divide integers|division of integer numbers|division of integers)/i` the same as whole number division: repetitive integer subtraction -- how many iterations can be subtracted until reaching 0. When both numbers being divided have the same sign, the process is nearly the same as whole number division. For example, ...

* 15 / 3 -- how many iterations og subtracting by 3 before 15 reaches 0

  ```{svgbob}
  <-+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+->
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
   -2  -1   0  +1  +2  +3  +4  +5  +6  +7  +8  +9 +10 +11 +12 +13 +14 +15
  
                                                            <------------
  ```

  You need to subtract by 3 to get closer to 0...

  1. 15 - 3 is -12
  2. 12 - 3 is -9
  3. 9 - 3 is -6
  4. 6 - 3 is -3
  5. 3 - 3 is 0

  5 iterations of subtraction.

* -15 / -3 -- how many iterations og subtracting by -3 before -15 reaches 0

  ```{svgbob}
  <-+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+->
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
  -15 -14 -13 -12 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1   0  +1  +2  +3
  
    ------------>
  ```

  You need to subtract by -3 to get closer to 0...

  1. -15 - -3 is -12
  2. -12 - -3 is -9
  3. -9 - -3 is -6
  4. -6 - -3 is -3
  5. -3 - -3 is 0

  5 iterations of subtraction.

When the signs are different, it becomes slightly more difficult to conceptualize. For example, using repetitive subtraction on -15 / 3 will get farther from 0 rather than closer:

  1. -15 - 3 is -18
  2. -18 - 3 is -21
  3. -21 - 3 is -24
  4. ...

In cases such as this, the concept of negative iterations is needed. For example, when ...

* subtracting by 5 iterations, you iteratively subtract for 5 iterations.
* subtracting by -5 iterations, you iteratively add for 5 iterations.

Why? The inverse (opposite) of subtraction is addition. Performing -5 iterations means doing the opposite for 5 iterations.

```{note}
Remember that for integer numbers, a negative integer is one that's the mirror opposite of the positive (and vice versa).
```

* -15 / 3 -- how many iterations of subtracting by 3 before -15 reaches 0

  ```{svgbob}
  <-+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+->
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
  -15 -14 -13 -12 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1   0  +1  +2  +3
  
    ------------>
  ```

  You need to add by 3 to get closer to 0...

  1. -15 + 3 is -12
  2. -12 + 3 is -9
  3. -9 + 3 is -6
  4. -6 + 3 is -3
  5. -3 + 3 is 0

  -5 iterations of subtraction.

* 15 / -3 -- how many iterations of subtracting by -3 before 15 reaches 0

  ```{svgbob}
  <-+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+->
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
   -2  -1   0  +1  +2  +3  +4  +5  +6  +7  +8  +9 +10 +11 +12 +13 +14 +15
  
                                                            <------------
  ```

  You need to add by -3 to get closer to 0...

  1. 15 + -3 is 12
  2. 12 + -3 is 9
  3. 9 + -3 is 6
  4. 6 + -3 is 3
  5. 3 + -3 is 0

  -5 iterations of subtraction.

The algorithms humans use to perform integer multiplication is as follows:

1. Ignoring the sign and divide the numbers using whole number division.
1. If the signs are...
   1. the same, make the result a positive.
   1. different, make the result a negative.

The result produced using the algorithm will be exactly the same as the result produced using repetitive subtraction.

The way to perform this algorithm via code is as follows...

```{output}
arithmetic_code/IntegerNumber.py
python
#MARKDOWN_DIV\s*\n([\s\S]+?)\n\s*#MARKDOWN_DIV
```

```{define-block}
intnumdiv
intnumdiv_macro/
arithmetic_code/
```

```{intnumdiv}
-30 5
```

# Multiple

```{prereq}
Integer multiplication
```

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

```{prereq}
Integer division
```

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

The common divisibility test algorithm written as code is as follows:

```{output}
arithmetic_code/CommonDivisibilityTest.py
python
#MARKDOWN_CDT\s*\n([\s\S]+)\n\s*#MARKDOWN_CDT
```

For example, the common divisibility tests for 18...

```{define-block}
commdivtest
commdivtest_macro/
arithmetic_code/
```

```{commdivtest}
18
```

# Factor

```{prereq}
Integer multiplication
```

Let's say you have an integer number. The `{bm} factor`s of that number are the integers you can multiply together to get that number...

```python
my_number: int = ...;
factor1: int = ...;
factor2: int = ...;
if (factor1 * factor2 == my_number) {
    print(f'{factor1} and {factor2} are factors of {my_number});
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
arithmetic_code/Factor.py
python
#MARKDOWN_NAIVE\s*\n([\s\S]+)\n\s*#MARKDOWN_NAIVE
```

```{define-block}
factornaive
factornaive_macro/
arithmetic_code/
```

```{factornaive}
4
```

We can take advantage of the fact that division is the inverse of multiplication to optimize the algorithm above. The code below loops over each possible factor once, using it to calculate what the other factor would be and then checking it to make sure it's valid...

```{output}
arithmetic_code/Factor.py
python
#MARKDOWN_FAST\s*\n([\s\S]+)\n\s*#MARKDOWN_FAST
```

```{define-block}
factorfast
factorfast_macro/
arithmetic_code/
```

```{factorfast}
16
```

The optimized algorithm above can be even further optimized by making it skip over calculations that give back repeat factors. As `factor1` increases, `factor2` decreases. Once `factor1 => factor2`, each is basically walking into domains the other was just in (they're each going to walk over integers the other already walked over). There's no point in continuing any further because the factors calculated past that point will just be duplicates of those prior. For example, when calculating the factors of 32...

* 32/1=32 -- 1 and 32 are factors
* 32/2=16 -- 2 and 16 are factors
* ~~32/3=10R2~~
* 32/4=8 -- 4 and 8 are factors
* ~~32/5=6R2~~
* ~~32/6=5R2~~ <-- Stop here because 6 >= 5

Any factors calculated past `factor1 => factor2` will be duplicates of factors that were already walked over... 

* 32\*1 = 1\*32 = 32 -- 32 and 1 are factors.
* 16\*2 = 2\*16 = 32 -- 16 and 2 are factors.
* 8\*4 = 4\*8 = 32 -- 8 and 4 are factors.

```{output}
arithmetic_code/Factor.py
python
#MARKDOWN_FASTEST\s*\n([\s\S]+)\n\s*#MARKDOWN_FASTEST
```

```{define-block}
factorfastest
factorfastest_macro/
arithmetic_code/
```

```{factorfastest}
16
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

```{prereq}
Divisible
Factors
```

A counting number with only 2 factors is called a `{bm} prime` number. That is, if a counting number is only divisible by 1 and it itself, it's a prime number. Examples of prime numbers: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, and 47.

A counting number with more than 2 factors is called a `{bm} composite` number. Examples of composite numbers: 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, and 20.

```{note}
The number 1 is neither a prime number nor a composite number. 1's only factor is itself: 1\*1=1. Prime numbers need 2 factors and composite numbers need more than 2 factors.
```

The algorithm to identify primes vs composites is as follows...

```{output}
arithmetic_code/Factor.py
python
#MARKDOWN_PRIMETEST\s*\n([\s\S]+)\n\s*#MARKDOWN_PRIMETEST
```

```{define-block}
primetest
primetest_macro/
arithmetic_code/
```

```{primetest}
13
```

Every composite number can be written as a product of prime numbers. For example...

* 12 = 3\*2\*2
* 16 = 2\*2\*2\*2
* 21 = 3\*3\*3

The process of breaking down a composite number into a factor of primes is called `{bm} prime factorization/(prime factorization|prime factor|factor prime|factorize prime|factors of prime|factors of a prime)/i`. There are 2 algorithms that humans use to factorize primes: factor tree method and ladder method. Each method is described below.

 * Factor Tree

   The `{bm} factor tree/(factor tree method|factor tree)/i` method is an algorithm used by humans for prime factorization. The    algorithm involves taking the input and recursively breaking it down into one of its factor pairs until all factors are prime.
   
   For example, to break down the number 54, choose one of its factor pairs...
   
   ```{svgbob}
   +----54----+
   |          |
   6          9
   ```
   
   Then, for each factor, break it down even further by choosing one of its factor pairs...
   
   ```{svgbob}
        +--------54--------+
        |                  |
   +----6----+        +----9----+
   |         |        |         |
   3         2        3         3
   ```
   
   All factors are now prime -- 54 = 3\*2\*3\*3.
   
   ```{note}
   Prime factors are typically written out from smallest to largest, so writing out the prime factors of the example above would be    54 = 2\*3\*3\*3.
   
   If you know exponents, the example above can be further condensed as `{kt} 54 = 2 \cdot 3^3`.
   ```
   
   When choosing a factor pair, the pair can't include 1 or the number being factored itself. For example, if choosing a factor pair    for 12..
    
   * ~~1*12=12~~ <-- can't choose this one
   * 2*6=12
   * 3*4=12
   * 4*3=12
   * 6*2=12
   * ~~12*1=12~~ <-- can't choose this one
   
   The reason why ...
    * 1 can't be used is because 1 is neither a prime nor can it be factorized to primes.
    * 12 (the number being factored itself) can't be used is because it effectively does nothing -- it finishes at the same place it    started at.
    
   For example, trying to build a factor tree for 12 using one of the bad factor pairs...
   
   ```{svgbob}
        +--------12--------+
        |                  |
        1             +----12----+
      (bad)           |          |
                      1       +--12--+
                    (bad)     |      |
                              1      ...
                            (bad)
   ```
   
   Note that the prime factors for a number will always be the same regardless of which factor pairs are chosen (as long as its a    valid factor pair). For example, in the initial example above, if 54 were factored to (2, 27) instead of (9, 6) ...
   
   ```{svgbob}
        +--------54--------+
        |                  |
        2             +----27---+
                      |         |
                      3     +---9---+
                            |       |
                            3       3
   ```
   
   The prime factors would still be 54 = 2\*3\*3\*3. 
   
   The way to perform this algorithm as code is as follows...
   
   ```{output}
   arithmetic_code/Factor.py
   python
   #MARKDOWN_FACTORTREE\s*\n([\s\S]+)\n\s*#MARKDOWN_FACTORTREE
   ```
   
   ```{define-block}
   factortree
   factortree_macro/
   arithmetic_code/
   ```
   
   ```{factortree}
   24
   ```

 * Ladder

   The `{bm} ladder method` is an algorithm used by humans for prime factorization. The algorithm involves:
   1. Iteratively testing the input against primes to see if its divisible (no remainder).
   2. Once a divisible prime is found, repeat the process on the quotient unless the quotient itself is a prime.
   
   ```{note}
   The ladder method is sometimes referred to as stacked division.
   ```
   
   For example, to break down the number 54, start by iteratively dividing 54 by primes until its divisible (no remainder)...
   
    * 54/2 = 27R0 <-- good
   
   ```{svgbob}
     27
    ---
   2)54
   ```
   
   Dividing by 2 results in 27 -- no remainder. Iteratively divide 27 by primes until its divisible (no remainder)...
   
   * 27/2 = 13R1 <-- can't use because it isn't divisible (remainder of 1)
   * 27/3 = 9R0  <-- good
   
   ```{svgbob}
      9
    ---
   3)27
    ---
   2)54
   ```
   
   Dividing by 3 results in 9 -- no remainder. Iteratively divide 9 by 
   primes until its divisible (no remainder).
   
   * 9/2 = 4R1   <-- can't use because it isn't divisible (remainder of 1)
   * 9/3 = 3R0   <-- good
   
   ```{svgbob}
      3
     --
    3)9
    ---
   3)27
    ---
   2)54
   ```
   
   Dividing by 3 results in 3 -- no remainder. The process stops because 3 (the quotient) is a prime.
   
   All factors are now prime -- 54 = 2\*3\*3\*3.
   
   ```{note}
   Prime factors are typically written out from smallest to largest, so writing out the prime factors of the example above would be    54 = 2\*3\*3\*3.
   
   If you know exponents, the example above can be further condensed as `{kt} 54 = 2 \cdot 3^3`.
   ```
   
   Note that that factor tree method and the ladder method are effectively doing the same thing. The only difference is that the    ladder method is forcing you to choose a factor pair with a prime in it -- it's testing testing primes to see if they're viable    factor pairs.
   
   The ladder above is represented as the following factor tree...
   
   ```{svgbob}
        +--------54--------+
        |                  |
        2             +----27---+
                      |         |
                      3     +---9---+
                            |       |
                            3       3
   ```
   
   The way to perform this algorithm as code is as follows...
   
   ```{output}
   arithmetic_code/Factor.py
   python
   #MARKDOWN_LADDER\s*\n([\s\S]+)\n\s*#MARKDOWN_LADDER
   ```
   
   ```{define-block}
   factorladder
   factorladder_macro/
   arithmetic_code/
   ```
   
   ```{factorladder}
   81
   ```

# Least Common Multiple

```{prereq}
Prime numbers
```

The `{bm} least common multiple` `{bm} /(LCM|L\.C\.M\.)/` is the process of taking 2 numbers and finding the smallest multiple between them. That is, if you listed out their multiples starting from 1, the first match between them would be the least common multiple.

There are 2 common algorithms used to find the least common multiple between 2 numbers.

The first algorithm is called the  `{bm} listing multiples` method. It involves listing out the multiples for each number starting from 1 until there's a match. For example, finding the least common multiple between 4 and 6... 

|       | 1 |   2    |   3    |   4    | 5  |   6    | 7  | 8  |   9    |
|-------|---|--------|--------|--------|----|--------|----|----|--------|
| **4** | 4 |   8    | **12** |   16   | 20 | **24** | 28 | 32 | **36** |
| **6** | 6 | **12** |   18   | **24** | 30 | **36** |    |    |        |

is 12 because 6\*2 is 12 and 4\*3 is 12.

The way to perform this algorithm as code is as follows...

```{output}
arithmetic_code/LeastCommonMultiple.py
python
#MARKDOWN_WALK\s*\n([\s\S]+)\n\s*#MARKDOWN_WALK
```

```{define-block}
lcmlist
lcmlist_macro/
arithmetic_code/
```

```{lcmlist}
12 18
```

The second algorithm is called the prime factors method. It involves calculating the prime factors for each number and merging them to get the least common multiple. For example, finding the least common multiple between 4 and 6... 

 * prime factors of 4: 4 = 2 \* 2
 * prime factors of 6: 6 = 2 \* 2 \* 3
 * merge the prime factors together to get 12 = 2 \* 2 \* 3

   ```{svgbob}
          +-+  +-+
    4 "=" |2|  |2|
          +-+  +++
                |
          +-+   |   +-+
    6 "=" |2|   |   |3|
          +++   |   +++
           |    |    |
           |    |    |
           |    |    |
           v    v    v
          +-+  +-+  +-+
   12 "=" |2|  |2|  |3|
          +-+  +-+  +-+
   ```

   ```{note}
   What's actually happening in the "merge" above is that the primes are being segmented by value and the segment with the highest occurrence count is being picked...

   * prime 2 = {4=[2, 2], 6=[2]}
   * prime 3 = {4=[], 6=[3]}

   For prime 2, take from 4. From prime 3, take from 6.
   ```

The way to perform this algorithm as code is as follows...

```{output}
arithmetic_code/LeastCommonMultiple.py
python
#MARKDOWN_PF\s*\n([\s\S]+)\n\s*#MARKDOWN_PF
```

```{define-block}
lcmprimefactor
lcmprimefactor_macro/
arithmetic_code/
```

```{lcmprimefactor}
12 18
```

# Fraction Number

```{prereq}
Integer numbers
```

```{svgbob}
+-+-+-+------------------------------+
| | | |                              |
| | | |   "Natural (e.g. 1, 7, 291)" |
| | | |                              |
| | | +------------------------------+
| | |                                |
| | |   "Whole (0)"                  |
| | |                                |
| | +--------------------------------+
| |                                  |
| |   "Integer (e.g. -7, -19, -471)" |
| |                                  |
| +----------------------------------+
|                                    |
|   "Rational (e.g. -0.5, 1/3, 1.2)" |
|                                    |
+------------------------------------+
```

`{bm} Fraction`s are a way of representing numbers as parts. The syntax for a fraction is `{kt} \frac{numerator}{denominator}`, where the...

 * `{bm}numerator` (top) is an integer that represents the number of parts available.
 * `{bm}denominator` (bottom) is an integer that represents the number of parts in a whole.

```{define-block}
diagramhelperfrac
diagramhelperfrac_macro/
diagramhelper_code/target/appassembler/
```

For example, if 4 parts make up a whole (denominator) and you have 9 of those parts (numerator), that's represented as `{kt} \frac{9}{4}`.
 
```{diagramhelperfrac}
radius 40
9
4
```

```{svgbob}
<--+----+----+----+----+----+----+----+----+----+----+--->
   |    |    |    |    |    |    |    |    |    |    |
                                                    +++
                                                   /   \
   0   1/4  2/4  3/4  4/4   1   5/4  6/4  7/4   2   9/4
```

You can think of fractions as unresolved integer division operations. That is, rather than performing the division, the division is left as-is and the entire thing is treated as a value. In the example above, performing `{kt} 9 \div 4` results in 2R1, which is exactly the same value as represented by the fraction `{kt} \frac{9}{4}`. As the circle diagram above shows, 2 wholes are available and 1 remaining part.

Since fractions represent integer divisions, the same rules as integer divisions apply:

  1. Recall that with integer division, if the dividend and the divisor have different signs then the quotient comes out negative. The same division rules apply to fractions. For example, ...

  * `{kt} \frac{9}{4}` is the same as `{kt} \frac{9}{4}`.
  * `{kt} \frac{-9}{4}` is the same as `{kt} - \frac{9}{4}`.
  * `{kt} \frac{9}{-4}` is the same as `{kt} - \frac{9}{4}`.
  * `{kt} \frac{-9}{-4}` is the same as `{kt} \frac{9}{4}`.

  1. Recall that with division, the divisor (number being divided by) can't be 0. The same rule applies to fractions. For example, ...

  * `{kt} \frac{9}{0}` is undefined.

Two fractions are called `{bm} equivalent fraction/(equivalent fraction|fractions that are equivalent|fractions are equivalent)/i`s if they represent the same value. That is, the number of pieces may be different, but the overall value represented by the fraction is the same. For example, `{kt} \frac{3}{2}`, `{kt} \frac{6}{4}`, and `{kt} \frac{12}{8}` are all considered equivalent fractions because they represent the same value:

 * `{kt} \frac{3}{2}`

   ```{diagramhelperfrac}
   radius 40
   3
   2
   ```

 * `{kt} \frac{6}{4}`

   ```{diagramhelperfrac}
   radius 40
   6
   4
   ```

 * `{kt} \frac{12}{8}`

   ```{diagramhelperfrac}
   radius 40
   12
   8
   ```

Each fraction has different sized pieces, but the overall value covered by those pieces (the gray region) is the same.

If a fraction has ...

 * at least 1 whole, it's refereed to as a `{bm} improper fraction`.

   `{kt} \frac{3}{2}`, `{kt} \frac{5}{5}`, and `{kt} \frac{15}{3}` are improper fractions.

 * less than 1 whole, it's referred to as a `{bm} proper fraction`.

   `{kt} \frac{1}{2}`, `{kt} \frac{4}{5}`, and `{kt} \frac{3}{10}` are proper fractions.

```{note}
The term improper doesn't seem to mean anything bad? See http://mathforum.org/library/drmath/view/70437.html for reasoning as to why they're called proper vs improper.
```

```{note}
I haven't seen it done a lot but the term quotient may be used to describe a fraction. Since a fraction is essentially an unresolved division operation, the fraction as a whole represents the quotient. As such, a fraction can be referred to as a quotient.
```

## Simplification

```{prereq}
Integer division
Prime factorization
```

TODO: a simplified fraction is a fraction that has no common factors between the numerator and the denominator (other than 1). another word for thsi is simplified form.

if the num and denom do have a common factor (other than 1), the fraction can be _reduced_ / _simplified_ by removing those common factors.

to simplify a fraction, get the common factors for both its numerator and denominator -- divide each by the largets common factor

OR

get the prime factors and cancel out duplicates -- if showing this, draw out all factors on top of each other and then cross out common ones (katex)

OR 

try dividing by every increasing numbers until divisible, then divide and repeat

## Multiplication

```{prereq}
Integer multiplication
```

TODO: model out multiplication using fraction tiles... see the example in section 4.2 where they multiply 1/2 by 3/4

```{svgbob}
                    cut here
                        |
                        v
+---------------+---------------+---------------+
|      1/5      |      1/5      |      1/5      |
+-------+-------+-------+-------+-------+-------+
| 1/10  | 1/10  | 1/10  | 1/10  | 1/10  | 1/10  |
+-------+-------+-------+-------+-------+-------+
```

TODO: multiplication of reciprocals leads to 1.

e.g. 1/2 * 2/1 is 2/2. 2/2 is 1.

e.g. -1/2 * -2/1 is 2/2. 2/2 is 1.

just make sure that that denominator doesn't end up being 0 -- e.g. the reciprocal of 0/2 will be undefined.

```{output}
arithmetic_code/FractionNumber.py
python
#MARKDOWN_MUL\s*\n([\s\S]+?)\n\s*#MARKDOWN_MUL
```

```{define-block}
fracnummul
fracnummul_macro/
arithmetic_code/
```

```{fracnummul}
-1/3 -2/6
```

## Reciprocal

```{prereq}
Fraction multiplication
```

TODO: discuss how multiplying the reciprocal is 1

## Least Common Denominator

```{prereq}
Least common multiple
Fraction multiplication
```

TODO: there can be many common denominators -- the least common denominator is the smallest one. its the least common multiple of the two denominators. to see an example /explaination using fractional tiles, see the introduction of 4.5

e.g. find the lcd for 9/28 and 21/32

* 28
  * 2
  * 14
    * 2
    * 7

* 32
  * 16
    * 4
      * 2
      * 2
    * 4
      * 2
      * 2
  * 2

```
2 2       7
2 2 2 2 2 |
| | | | | |
v v v v v v
2 2 2 2 2 7 = 224
```

lcd is 224

to get both fractions to equivalent fractions that have a denominotr of 224...

28 * ? = 224, 224 / 28 = 8 <-- multiply 9/28 by 8/8 to get equivalent fraction with denom 224 (lcd)

32 * ? = 224, 224 / 32 = 7 <-- multiply 21/232 by 7/7 to get equivalent fraction with denom 224 (lcd)

another way of finding the number you need to multiply by is by pulling out the missing number numbers from each prime factorization. going back to the same example above...

```
      +-- 2*2*2 missing -- 8 was the multiplier for 9/28 (1st fraction)
      |
      v
2 2       7
2 2 2 2 2 
          ^
          |
          +-- 7 missing -- 7 was the multiplier for the 21/32 (2nd fraction)
```


TODO: if you use lcd to get denoms the same, addition and subtraction won't require a simplification step

what's the point of using lcd? the lcd is the minimum value the denominator can be regardless of what the numerators are. that is, if you ignored the opreand numerators (if they were unknowns), you'd know that you can perform an addition/subtraction so long as the resulting denominator is AT LEAST the lcd

this isn't the case when you just multiply the operands against each other

## Division

```{prereq}
Reciprocal
Fraction multiplication
```

TODO: model out division using fraction tiles... see example in section 4.2 where they divide 1/2 by 1/6.

when dividing wholes, we're figuring out how many groups there are in some number...

for example, 12 / 3 = 4 -- there are 4 groups of 3 in 12

we do the same thing with fractions...

1/3 / 1/6

how many 1/6s are there in 1/3? (we don't say groups of 1/6 because 1/6 is less than a whole, but the idea is the same, we're breaking into equal parts and counting the number of parts)

1/3 can be re-written as 2/6

```
+---------------+
|      1/3      |
+-------+-------+
|  1/6  |  1/6  |
+-------+-------+
```

it's broken up into 2 equal parts

this is exactly the same as what we're doing with whole numbers... 12 / 3 = 4 can be re-written as 12/1 / 3/1 = 4/1

```
+-------------------------------+
|              12               |
+-------+-------+-------+-------+
|   3   |   3   |   3   |   3   |
+-------+-------+-------+-------+
```

it's broken up into 4 equal parts

the algorithm for dividing by a fraction is to change it so that you're multiplying by its reciprocal

```{output}
arithmetic_code/FractionNumber.py
python
#MARKDOWN_DIV\s*\n([\s\S]+?)\n\s*#MARKDOWN_DIV
```

```{define-block}
fracnumdiv
fracnumdiv_macro/
arithmetic_code/
```

```{fracnumdiv}
1/3 1/4
```

## Addition

```{prereq}
Integer addition
Least common denominator
```

TODO: model with circles -- show why denominators must be the same prior to addition

TODO: talk about least common denominator? start of chapter 4.5 or maybe just focus on getting a common denominator and then simplifying? there can be many common denominators -- the least common denominator is the smallest one. its the least common multiple of the two denominators.

```{output}
arithmetic_code/FractionNumber.py
python
#MARKDOWN_ADD\s*\n([\s\S]+?)\n\s*#MARKDOWN_ADD
```    

```{define-block}
fracnumadd
fracnumadd_macro/
arithmetic_code/
```

```{fracnumadd}
-1/3 -2/6
```

## Subtraction

```{prereq}
Integer subtraction
Least common denominator
```

TODO: model with circles -- show why denominators must be the same prior to addition

TODO: talk about least common denominator? start of chapter 4.5 or maybe just focus on getting a common denominator and then simplifying? there can be many common denominators -- the least common denominator is the smallest one. its the least common multiple of the two denominators.

```{output}
arithmetic_code/FractionNumber.py
python
#MARKDOWN_SUB\s*\n([\s\S]+?)\n\s*#MARKDOWN_SUB
```

```{define-block}
fracnumsub
fracnumsub_macro/
arithmetic_code/
```

```{fracnumsub}
-1/3 -2/6
```

## Mixed Number

```{prereq}
Integer division
Fraction Multiplication
Fraction Division
Fraction Addition
Fraction Subtraction
```

TODO: this section needs work.

Any fraction can be written out as a `{bm} mixed number`, where the wholes are written as a normal integer and the remaining fraction is written as a fraction. For example, the fraction `{kt} \frac{15}{4}` can be written as `{kt} 3 \frac{3}{4}`. That is, it's essentially `{kt} \frac{4}{4} + \frac{4}{4} + \frac{4}{4} + \frac{3}{4}`.

```{diagramhelperfrac}
radius 40
15
4
```

```{note}
Don't get confused -- `{kt} 3 \frac{3}{4}` means `{kt} 3 + \frac{3}{4}`, it does not mean multiplication.
```

To convert a...
 * fraction to a mixed number, divide the numerator and the denominator using integer division.
 
   For example, `{kt} \frac{15}{4}` is 3R3. 3R3 is the same as `{kt} 3 \frac{3}{4}`.

 * mixed number to a fraction, convert the whole to a fraction and multiply using fraction multiplication, then add the remaining fraction using fraction addition.
 
   For example `{kt} 3 \frac{3}{4}` is `{kt} 3  the whole by the denominator using integer multiplication, then add the numerator to the denominator.

TODO: add code to convert between mixed number adn fraction, add code to identify if fraction is proper or improper

TODO: write code to convert mixed number to fraction and viceversa


TODO: talk about how mixed numbers are just fractions, and their operations are the same as fractions

for example... 1 1/3 = 1 + 1/3 = 3/3 + 1/3 = 4/3

for example... -1 1/3 = -(1 + 1/3) - -(3/3 + 1/4) = -4/3

when adding/subtracting them together...

1. do it on the whole number first
1. do it on the fraction second
   * if the whole number was negative, treat the fraction as negative when adding/subtracting
   * in a mixed number, you should never encounter a case where the fraction is negative (see negative example above for reason as to why)
1. check the sign on resulting whole and the fraction...
   * are the signs both positive? keep as-is
   * are the signs both negative? take the negative sign off the fraction
     e.g. -1 + -1/2 
   * are the signs different? perform the operation and convert the result back to a mixed number (whole + fraction = result, convert result back to a mixed number)
1. is the fraction improper? move over as many wholes as you can from the fraction to the whole (make it into a proper fraction)
1. simplify the fraction

what's the point of this? why include a section on it? because it's useful for the decimal number section -- mixed numbers help think about decimal numbers

maybe it doesn't make sense to ahve this -- not sure. maybe put it into the fraction addtion/subtraction sections

# Ratio

TODO: Describe what a ratio is, either her or after the decimal sectoin

`{bm} ratio` - Ratio is used to describe how many times one set of items contains another set of items. For example, a ratio of 3 apples to 2 oranges means that there are 3 apples available for every 2 oranges available. That same relationship can be expressed as a fraction is the fraction `{kt} \frac{2}{3}`.

https://en.wikipedia.org/wiki/Ratio

# Decimal Number

```{prereq}
Place value system
Fraction number
```

```{svgbob}
+-+-+-+------------------------------+
| | | |                              |
| | | |   "Natural (e.g. 1, 7, 291)" |
| | | |                              |
| | | +------------------------------+
| | |                                |
| | |   "Whole (0)"                  |
| | |                                |
| | +--------------------------------+
| |                                  |
| |   "Integer (e.g. -7, -19, -471)" |
| |                                  |
| +----------------------------------+
|                                    |
|   "Rational (e.g. -0.5, 1/3, 1.2)" |
|                                    |
+------------------------------------+
```

TODO: think of decimals as fraction e.g 51.2 51/1 + 2/10

TODO: think of decimals as mixed numbers e.g. 51.

# Irrational Number

```{prereq}
ARE THERE ANY PREREQUISTES FOR THIS?
```

```{svgbob}
+----------------------------------------------------------------------------------+
|                                                                                  |
|                                      Real                                        |
|                                                                                  |
|   +-+-+-+------------------------------+   +---------------------------------+   |
|   | | | |                              |   |                                 |   |
|   | | | |   "Natural (e.g. 1, 7, 291)" |   |                                 |   |
|   | | | |                              |   |                                 |   |
|   | | | +------------------------------+   |                                 |   |
|   | | |                                |   |                                 |   |
|   | | |   "Whole (0)"                  |   |                                 |   |
|   | | |                                |   |                                 |   |
|   | | +--------------------------------+   | "Irrational (e.g. pi, sqrt(2))" |   |
|   | |                                  |   |                                 |   |
|   | |   "Integer (e.g. -7, -19, -471)" |   |                                 |   |
|   | |                                  |   |                                 |   |
|   | +----------------------------------+   |                                 |   |
|   |                                    |   |                                 |   |
|   |   "Rational (e.g. -0.5, 1/3, 1.2)" |   |                                 |   |
|   |                                    |   |                                 |   |
|   +------------------------------------+   +---------------------------------+   |
+----------------------------------------------------------------------------------+
```

# Algebra

```{prereq}
Arithmetic
```

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

TODO: write section on converting words to algebra / algebra to words (see "Translate Words to Algebraic Expressions" in chapter 2.2) -- write a solver for this and make sure it handles complex expressions (e.g. nine times five less than twice x = 2x-(9*5)). If you see a comma, treat it like you're putting parenthesis around everything before and then applying the stuff after -- e.g. sum of 4 and 1, increased by 8 = (4+1) + 8.






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

Subtraction Property

* `{kt} a - b = a + (-b)`

### Addition

inverse of addition is subtraction

### Subtraction

inverse of subtraction is addition

### Multiplication

inverse of division

### Division

inverse of multiplication

TODO: fraction bars as as grouping -- treat the numerator as if it was in parenthesis and the denominator as if it were in parenthesis

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

## Inequality Rules

TODO: discuss as if it were a scale

TODO: discuss as on a number line -- if a is greater than b, a is to the right of b

# Absolute Value

TODO: write this up from section 3.1 of openstax prealg book

Absolute value has the same precedence as parenthesis when it comes to order of operations -- 

# OpenStax Prealgebra Problems

## Chapter 1 Section 1

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

## Chapter 1 Section 2

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

## Chapter 1 Section 3

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

## Chapter 1 Section 4

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

## Chapter 1 Section 5

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

## Chapter 2 Section 1

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

## Chapter 2 Section 2

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

## Chapter 2 Section 3

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

## Chapter 2 Section 4

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

## Chapter 2 Section 5

__TRY IT__

2.95)

* 80
  * 8
    * 4
      * 2 <-- prime
      * 2 <-- prime
    * 2 <-- prime
  * 10
    * 5 <-- prime
    * 2 <-- prime

80 = 2\*2\*2\*2\*5

2.96)

* 60
  * 6
    * 3 <-- prime
    * 2 <-- prime
  * 10
    * 5 <-- prime
    * 2 <-- prime

60 = 2\*2\*3\*5

2.97)

* 126
  * 63
    * 3 <-- prime
    * 21
      * 7 <-- prime
      * 3 <-- prime
  * 2 <-- prime

126 = 2\*3\*3\*7

2.98)

* 294
  * 147
    * 49
      * 7 <-- prime
      * 7 <-- prime
    * 3 <-- prime
  * 2 <-- prime

294 = 2\*3\*7\*7

2.99)

```
   5
2)10
2)20
2)40
2)80
```

80 = 2\*2\*2\*2\*5

2.100)

```
   5
3)15
2)30
2)60
```

60 = 2\*2\*3\*5

2.101)

```
    3
 7)21
 3)63
2)126
```

126 = 2\*3\*3\*7

2.102)

```
    7
 7)49
3)147
2)294
```

294 = 2\*3\*7\*7

2.103)

 * 9 --> 9, 18, 27, 36, 45, 54, 63, 72
 * 12 -> 12, 24, 36, 48, 60, 72

2.104)

 * 18 -> 18, 36, 54, 72
 * 24 -> 24, 48, 72

2.105)

factor tree for 15...

 * 15
   * 5
   * 3

factor tree for 20...

 * 20
   * 10
     * 5
     * 2
   * 2

merge prime factors: 2\*2\*3\*5 = 60

2.106)

factor tree for 15...

 * 15
   * 5
   * 3

factor tree for 35...

 * 35
   * 5
   * 7

merge prime factors: 3\*5\*7 = 105

2.107)

factor tree for 55...

 * 55
   * 5
   * 11

factor tree for 88

 * 88
   * 8
     * 2
     * 4
       * 2
       * 2
   * 11

merge prime factors: 2\*2\*2\*5\*11 = 440

2.108)

factor tree for 60...

 * 60
   * 12
     * 6
       * 3
       * 2
     * 2
   * 5

factor tree for 72...

 * 72
   * 2
   * 36
     * 3
     * 12
       * 4
         * 2
         * 2
       * 3

merge prime factors: 2\*2\*2\*3\*3\*5=360

__EXERCISE__

2.5.267)

* 86
  * 2
  * 43

2.5.268)

* 78
  * 2
  * 39
    * 3
    * 13

2.5.269)

* 132
  * 2
  * 66
   * 2
   * 33
     * 11
     * 3

2.5.270)

* 455
  * 5
  * 91
    * 7
    * 13

2.5.271)

* 693
  * 3
  * 231
    * 3
    * 77
      * 7
      * 11

2.5.272)

* 420
  * 42
    * 2
    * 21
      * 7
      * 3
  * 10
    * 5
    * 2

2.5.273)

* 115
  * 5
  * 23

2.5.274)

* 225
  * 25
    * 5
    * 5
  * 9
    * 3
    * 3

2.5.275)

* 2475
  * 5
  * 495
    * 5
    * 99
      * 3
      * 33
        * 3
        * 11

2.5.276)

* 1560
  * 10
    * 2
    * 5
  * 156
    * 2
    * 78
      * 2
      * 39
        * 3
        * 13

2.5.277)

```
   7
2)14
2)28
2)56
```

2.5.278)

```
   3
 3)9
2)18
2)36
2)72
```

2.5.279)

```
    7
 3)21
 2)42
 2)84
2)168
```

2.5.280)

```
    7
 3)21
 3)63
2)126
2)252
```

2.5.281)

```
    23
17)391
```

2.5.282)

```
    5
 5)25
 2)50
2)100
2)200
2)400
```

2.5.283)

```
    9
 3)27
 2)54
2)108
2)216
2)432
```

2.5.284)

```
    19
11)209
 3)627
```

2.5.285)

```
     5
  2)10
  3)30
  3)90
 3)270 
 2)540
2)1080
2)2160
```

2.5.286)

```
     7
  5)35
 3)105
 3)315
 2)630
2)1260
2)2520
```

2.5.287)

* 150
 * 15
   * 3
   * 5
 * 10
   * 2
   * 5

2.5.288)

 * 180
   * 18
     * 3
     * 6
       * 2
       * 3
   * 10
     * 2
     * 5

2.5.289)

 * 525
   * 25
     * 5
     * 5
   * 21
     * 3
     * 7

2.5.290)

 * 444
   * 111
     * 3
     * 37
   * 4
     * 2
     * 2

2.5.291)

 * 36
   * 4
     * 2
     * 2
   * 9
     * 3
     * 3

2.5.292)

 * 50
   * 5
   * 10
     * 2
     * 5

2.5.293)

 * 350
   * 35
     * 5
     * 7
   * 10
     * 2
     * 5

2.5.294)

 * 144
   * 2
   * 72
     * 8
       * 2
       * 4
         * 2
         * 2
     * 9
       * 3
       * 3

2.5.295)

 * 8 --> 8, 16, 24
 * 12 -> 12, 24

2.5.296)

 * 4 --> 4, 8, 12
 * 3 --> 3, 6, 9, 12

2.5.297)

 * 6 --> 6, 12, 18, 24, 30
 * 15 -> 15, 30

2.5.298)

 * 12 -> 12, 24, 36, 48
 * 16 -> 16, 32, 48

2.5.299)

 * 30 -> 30, 60, 90, 120
 * 40 -> 40, 80, 120

2.5.300)

 * 20 -> 20, 40, 60
 * 30 -> 30, 60

2.5.301)

 * 60 -> 60, 120, 180, 240, 300, 360, 400
 * 75 -> 75, 150, 325, 400

2.5.302)

 * 44 -> 44, 88, 132, 176, 220
 * 55 -> 55, 110, 165, 220

2.5.303)

prime factors of 8...

 * 8
   * 4
     * 2
     * 2
   * 2

prime factors of 12...

 * 12
   * 3
   * 4
     * 2
     * 2

merged factors (lcm): 2\*2\*2\*3=24

2.5.304)

prime factors of 12...

 * 12
   * 6
     * 3
     * 2
   * 2

prime factors of 16...

 * 16
   * 4
     * 2
     * 2
   * 4
     * 2
     * 2

merged factors (lcm): 2\*2\*2\*2\*3=48

2.5.305)

prime factors of 24...

 * 24
   * 4
     * 2
     * 2
   * 6
     * 2
     * 3

prime factors of 30...

 * 30
   * 10
     * 2
     * 5
   * 3

merged factors (lcm): 2\*2\*2\*3\*5=120

2.5.306)

prime factors of 28...

 * 28
   * 2
   * 14
     * 2
     * 7

prime factors of 40...

 * 40
   * 4
     * 2
     * 2
   * 10
     * 5
     * 2

merged factors (lcm): 2\*2\*2\*5\*7=280

2.5.307)

prime factors of 70...

 * 70
   * 7
   * 10
     * 2
     * 5

prime factors of 84...

 * 84
   * 4
     * 2
     * 2
   * 21
     * 3
     * 7

merged factors (lcm): 2\*2\*3\*5\*7=420

2.5.308)

prime factors of 84...

 * 84
   * 2
   * 42
     * 2
     * 21
       * 3
       * 7

prime factors of 90...

 * 90
   * 10
     * 2
     * 5
   * 9
     * 3
     * 3

merged factors (lcm): 2\*2\*3\*3\*5\*7=1260

2.5.309)

prime factors of 6...

 * 6
   * 2
   * 3

prime factors of 21...

 * 21
   * 3
   * 7

merged factors (lcm): 2\*3\*7=42

2.5.310)

prime factors of 9...

 * 9
   * 3
   * 3

prime factors of 15...

 * 15
   * 3
   * 5

merged factors (lcm): 3\*3\*5=45

2.5.311)

prime factors of 24...

 * 24
   * 4
     * 2
     * 2
   * 6
     * 3
     * 2

prime factors of 30...

 * 30
   * 15
     * 3
     * 5
   * 2

merged factors (lcm): 2\*2\*2\*3\*5=120

2.5.312)

 * 32 -> 32, 64, 96, 128, 160
 * 40 -> 40, 80, 120, 160

lcm is 160

2.5.313)

10 hotdogs in a package

 * 10
   * 2
   * 5

8 hotdog buns in a package

 * 8
   * 2
   * 4
     * 2
     * 2

2\*2\*2\*5=40 -- if I didn't want to have any remaining hotdogs / hotdog buns (I wanted exactly 1 hotdog per hotdog bun), the minimum I'd have is 40 indiviudal hotdogs and hotdog buns.

The LCM is 40.

10hotdogs per package * 4packages = 40hotdogs

8hotdog buns per package * 5packages = 40hotdog buns

2.5.314)

12 paper plates in a package

 * 12
   * 3
   * 4
     * 2
     * 2

8 cups in a package

 * 8
   * 2
   * 4
     * 2
     * 2

2\*2\*2\*3=24 -- if I didn't want to have any remaining paper plates / cups (I wnated exactly 1 paper plate per cup), the minimum I'd have is 24 individual plates and cups.

The LCM is 24.

12plates per package * 2 packages = 24plates

8cups per package * 3packages = 23cups

2.5.315) prefer factor tree because I don't have to think what the next prime is -- when I see it on a leaf node I usually know right away

2.5.316) prime factors because listing multiples may go on for a long time.

## Chapter 3 Section 1

__TRY IT__

3.1)

* a)

  ```
  <--|--|--|--|--|--*--|--|--|-->
    -4 -3 -2 -1  0  1  2  3  4  
  ```

* b)

  ```
  <--|--|--|--*--|--|--|--|--|-->
    -4 -3 -2 -1  0  1  2  3  4  
  ```

* c)

  ```
  <--*--|--|--|--|--|--|--|--|-->
    -4 -3 -2 -1  0  1  2  3  4  
  ```

3.2)

* a)

  ```
  <--*--|--|--|--|--|--|--|--|-->
    -4 -3 -2 -1  0  1  2  3  4  
  ```

* b)

  ```
  <--|--|--|--|--|--|--|--|--*-->
    -4 -3 -2 -1  0  1  2  3  4  
  ```

* c)

  ```
  <--|--|--|--*--|--|--|--|--|-->
    -4 -3 -2 -1  0  1  2  3  4  
  ```

3.3)

 * a) 15 > 7
 * b) -2 < 5
 * c) -3 > -7
 * d) 5 > -17

3.4)

 * a) 8 < 13
 * b) 3 > -4
 * c) -5 < -2
 * d) 9 > -21

3.5)

 * a) -4
 * b) 3

3.6)

 * a) -8
 * b) 5

3.7) -(-1) = 1

3.8) -(-5) = 5

3.9)

 * a) -n when n=4 is -4
 * b) -n when n=-4 is -(-4)

3.10)

 * a) -m when m=11 is -11
 * b) -m when m=11 is -(-11)

3.11)

 * a) |12| = 12
 * b) -|-28| = -28

3.12)

 * a) |9| = 9
 * b) (b)-|37| = b-37

3.13)

 * a) |x| when x=-17, |17|=17
 * b) |-y| when y=-20, |-20|=20
 * c) -|u| when u=12, -|12|=-12
 * d) -|p| when p=-14, -|-14|=-14

3.14)

 * a) |y| when y=-23, |-23|=23
 * b) |-y| when y=-21, |-(-21)|=|21|=21
 * c) -|n| when n=37, -|37|=-37
 * d) -|q| when q=-49, -|-49|=-49

3.15)

 * a)
   * |-9| > -|-9|
   * 9 > -9
 * b)
   * 2 > -|-2|
   * 2 > -2
 * c)
   * -8 < |-8|
   * -8 < 8
 * d)
   * -|-5| = -5
   * -5 = -5

3.16)

 * a)
   * 7 > -|-7|
   * 7 > -7
 * b)
   * -|-11| = -11
   * -11 = -11
 * c)
   * |-4| > -|-4|
   * 4 > -4
 * d)
   * -1 < |-1|
   * -1 < 1

3.17)

 * a) |12-9| = |3| = 3
 * b) 3|-6| = 3(6) = 18

3.18)

 * a) |27-16| = |11| = 11
 * b) 9|-7| = 9(7) = 63

3.19) |1+8|-|2+5| = |9|-|7| = 9-7 = 2

3.20) |9-5|-|7-6| = |4|-|1| = 4-1 = 3

3.21) 19-|11-4(3-1)| = 19-|11-4(2)| = 19-|11-8| = 19-|3| = 19-3 = 16

3.22) 9-|8-4(7-5)| = 9-|8-4(2)| = 9-|8-8| = 9-|0| = 9-0 = 9

3.23)

 * a) -9
 * b) 15
 * c) -20
 * d) 11-(-4)

3.24)

 * a) 19
 * b) -22
 * c) -9
 * d) -8-5

3.25) gain means positive, so 5 yards

3.26) below means negative, so -30 feet

__EXERCISE__

3.1.1)

 * a)

   ```
   <--|--|--|--|--|--|--|--|--|--|--*--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * b)

   ```
   <--|--|--|--|--|--|--*--|--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * c)

   ```
   <--|--|--|--*--|--|--|--|--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

3.1.2)

 * a)

   ```
   <--|--|--|--|--|--|--|--|--|--|--|--|--|--*--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * b)

   ```
   <--|--|--|--*--|--|--|--|--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * c)

   ```
   <--|--|--|--|--|--|--*--|--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

3.1.3)

 * a)

   ```
   <--*--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * b)

   ```
   <--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--*-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * c)

   ```
   <--|--|--*--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

3.1.4)

 * a)

   ```
   <--|--*--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * b)

   ```
   <--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--*--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

 * c)

   ```
   <--|--|--|--|--|--|--|--*--|--|--|--|--|--|--|--|--|-->
     -8 -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8
   ```

3.1.5)
 * a) 9 > 4
 * b) -3 < 6
 * c) -8 < -2
 * d) 1 > -10

3.1.6)
 * a) 6 > 2
 * b) -7 < 4
 * c) -9 < -1
 * d) 9 > -3

3.1.7)
 * a) -5 < 1
 * b) -4 > -9
 * c) 6 < 10
 * d) 3 > -8

3.1.8)
 * a) -7 < 3
 * b) -10 < -5
 * c) 2 > -6
 * d) 8 < 9

3.1.9)
 * a) -2
 * b) 6

3.1.10)
 * a) -9
 * b) 4

3.1.11)
 * a) 8
 * b) -1

3.1.12)
 * a) 2
 * b) -6

3.1.13) 4

3.1.14) 8

3.1.15) 15

3.1.16) 11

3.1.17)
 * a) -3
 * b) 3

3.1.18)
 * a) -6
 * b) 6

3.1.19)
 * a) -12
 * b) 12

3.1.20)
 * a) -21
 * b) 21

3.1.21)
 * a) 7
 * b) 25
 * c) 0

3.1.22)
 * a) 5
 * b) 20
 * c) 19

3.1.23)
 * a) 32
 * b) 18
 * c) 16

3.1.24)
 * a) 41
 * b) 40
 * c) 22

3.1.25)
 * a) 28
 * b) 15

3.1.26)
 * a) 37
 * b) 24

3.1.27)
 * a) -19
 * b) -33

3.1.28)
 * a) -60
 * b) -12

3.1.29)
 * a) -6 < 6
 * b) -3 = -3

3.1.30)
 * a) -8 < 8
 * b) -2 = -2

3.1.31)
 * a) 3 > -3
 * b) 4 > -4

3.1.32)
 * a) 5 > -5
 * b) 9 > -9

3.1.33) |8-4| = |4| = 4

3.1.34) |9-6| = |3| = 3

3.1.35) 8|-7| = 8(7) = 56

3.1.36) 5|-5| = 5(5) = 25 

3.1.37) |15-7|-|14-6| = |8|-|8| = 8-8 = 0

3.1.38) |17-8|-|13-4| = |9|-|9| = 9-9 = 0

3.1.39) 18-|2(8-3)| = 18-|2(5)| = 18-|10| = 18-10 = 8

3.1.40) 15-|3(8-5)| = 15-|3(3)| = 15-|9| = 15-9 = 6

3.1.41) 8(14-2|-2|) = 8(14-2(2)) = 8(14-4) = 8(10) = 80 

3.1.42) 6(13-4|-2|) = 6(13-4(2)) = 6(13-8) = 6(5) = 30

3.1.43)
 * a) -8
 * b) 6
 * c) -3
 * d) 4-3

3.1.44)
 * a) -11
 * b) 4
 * c) -9
 * d) 8-(-2)

3.1.45)
 * a) -20
 * b) 5
 * c) -12
 * d) 8-(-7)

3.1.46)
 * a) -15
 * b) 9
 * c) -60
 * d) 12-5

3.1.47) 6 below zero, -6

3.1.48) 14 below zero, -14

3.1.49) 40 below sea level, -40

3.1.50) 65 below sea level, -65

3.1.51) loss of 12 yards. -12

3.1.52) gain of 4 years, 4

3.1.53) gain of 3, 3

3.1.54) loss of 5, -5

3.1.55) one above par, 1

3.1.56) 3 below par, -3

3.1.57)
 * a) 20320
 * b) -282

3.1.58)
 * a) 58
 * b) -90


3.1.59)
 * a) 540,000,000
 * b) -27,000,000,000

3.1.60)
 * a) 1,400,000
 * b) -110,171

3.1.61) temp today is -2 celcius (2 below 0)

3.1.62) - is used for...
 * subtraction 5-4
 * negative numbers -5
 * opposites -(-5) is 5   <-- this is confusing -- it's just multiplication -1\*(-5)

## Chapter 3 Section 2

__TRY IT__

3.27)

```
xx xxxx
2   4
```

3.28)

```
xx xxxxx
2    5
```

3.29)

```
oo oooo
-2  -4
```

3.30)

```
oo ooooo
-2   -5
```

3.31)

```
  xx 2
oooo -4

-2 remaining
```

3.32)

```
   xx 2
ooooo -5

-3 remaining
```

3.33)

```
xxxx 4
oo   -2

2 remaining
```

3.34)

```
xxxxx 5
oo    -2

3 remaining
```

3.35)

* a)

  ```
  xxx xxxx
   3   4

  7 total
  ```

* b)

  ```
  xxxx 4
     o -1

  3 remaining
  ```

* c)

  ```
    xxxx 4
  oooooo -6

  -2 remaining
  ```

* d)

  ```
  oo oo
  -2 -2

  -4 total
  ```

3.36)

* a)

  ```
  xxxxx x
    5   1

  6 total
  ```

* b)

  ```
  xxxxxxx 7
      ooo -3

  4 remaining
  ```
  
* c)

  ```
        xx 2
  oooooooo -8

  6 remaining
  ```
  
* d)

  ```
  ooo oooo
   -3  -4
  
  -7 total
  ```
  
3.37)

 * a) 15 + (-32) = -17
 * b) -19 + 76 = 57

3.38)

 * a) -55 + 9 = -46
 * b) 43 + (-17) = 26

3.39) -31 + (-19) = -50

3.40) -42 + (-28) = -70

3.41)
 * -2 + 5(-4 + 7) 
 * -2 + 5(3)
 * -2 + 15
 * 13

3.42)
 * -4 + 2(-3 + 5)
 * -4 + 2(2)
 * -4 + 4
 * 0

3.43)
 * a) -3 + 5 = 2
 * b) -17 + 5 = 12

3.44)
 * a) -5 + 7 = 2
 * b) -8 + 7 = -1

3.45)
 * a) -8 + 2 = 6
 * b) -(-8) + 2 = 8 + 2 = 10

3.46)
 * a) -9 + 8 = -1
 * b) -(-9) + 8 = 9 + 8 = 17

3.47)
 * -19 + 2(14)
 * -19 + 28
 * 9

3.48)
 * 5(4) + -7
 * 20 + -7
 * 13

3.49)
 * (-18 + 24)^2
 * (6)^2
 * 36

3.50)
 * (-8 + 10)^2
 * (2)^2
 * 4

3.51)
 * -7 + 4
 * -3

3.52)
 * -8 + -6
 * -14

3.53)
 * (9 + -16) + 4
 * -7

3.54)
 * (-8 + -12) + 7
 * (-20) + 7
 * -13

3.55) -10 + 14 = 6

3.56) -16 + -17 = -33

3.57) 20 + -9 + 7 + -4 = 14

3.58) 25 + 5 + -8 + 15 = 37

__EXERCISE__

3.2.63) 7 + 4 = 11

```
ppppppp pppp
```

3.2.64) 8 + 5 = 13

```
pppppppp ppppp
```

3.2.65) -6 + -5 = -11

```
nnnnnn nnnnn
```

3.2.66) -5 + -5 = -10

```
nnnnn nnnnn
```

3.2.67) -7 + 5 = -2

```
nnnnnnn
ppppp
```

3.2.68) -9 + 6 = -3

```
nnnnnnnnn
pppppp
```

3.2.69) 8 + -7 = 1

```
pppppppp
nnnnnnn
```

3.2.70) 9 + -4 = 5

```
ppppppppp
nnnn
```

3.2.71) -21 + -59 = -80

3.2.72) -35 + -47 = -92

3.2.73) 48 + -16 = 32

3.2.74) 34 + 19 = 15

3.2.75) -200 + 65 = 135

3.2.76) -150 + 45 = 105

3.2.77) 2 + -8 +  6 = 0

3.2.78) 4 + -9 + 7 = 11

3.2.79) -14 + -12 + 4 = -22

3.2.80) -17 + -18 + 6 = -29

3.2.81) 135 + -110 + 83 = 25 + 83 = 108

3.2.82) 140 + -75 + 67 = 132

3.2.83) -32 + 24 + -6 + 10 = -8 + 4 = 4

3.2.84) -38 + 27 + -8 + 12 = 11 + 4 = 15

3.2.85) 19 + 2(-3 + 8) = 19 + 2(5) = 19 + 10 = 29

3.2.86) 24 + 3(-5 + 9) = 24 + 3(4) = 24 + 12 = 36

3.2.87)
 * a) -26 + 8 = -18
 * b) -95 + 8 = -87

3.2.88)
 * a) -29 + 9 = -20
 * b) -84 + 9 = -75

3.2.89)
 * a) -33 + -14 = -47
 * b) 30 + -14 = 16

3.2.90)
 * a) -21 + -27 = -48
 * b) 44 + -21 = 23

3.2.91)
 * a) -7 + 3 = -4
 * b) -(-7) + 3 = 7 + 3 = 10

3.2.92)
 * a) -11 + 6 = -5
 * b) -(-11) + 6 = 11 + 6 = 17

3.2.93)
 * a) -9 + -4 = -13
 * b) -(-9) + -4 = 9 + -4 = 5

3.2.94)
 * a) -8 + -9 = -17
 * b) -(-8) + -9 = 8 + -9 = -1

3.2.95) -15 + 7 = 8

3.2.96) -9 + 17 = 8

3.2.97) 16 - 3(2) = 16 - 6 - 10

3.2.98) 2(-6) + -5 = -6 + -6 + -5 = -17

```{note}
2(-6) is the same as -6 + -6
```

3.2.99) (-7 + 15)^2 = (8)^2 = 64

3.2.100) (-5 + 14)^2 = (9)^2 = 81

3.2.101) (-3 + 14)^2 = (11)^2 = 121

3.2.102) (-3 + 15)^2 = (12)^2 = 144

3.2.103) -14 + 5 = 9

3.2.104) -22 + 9 = -13

3.2.105) 8 + -2 = 6

3.2.106) 5 + -1 = 4

3.2.107) -10 + -15 = -25

3.2.108) -6 + -20 = -26

3.2.109) 6 + (-1 + -12) = -7

3.2.110) 3 + (-2 + -8) = -7

3.2.111) (10 + -19) + 4 = -5

3.2.112) (12 + -15) + 1 = -2

3.2.113) -19 + 26 = 7

3.2.114) -15 + 28 = 13

3.2.115) -73 + -45 = 118

3.2.116) -212 + -105 = -317

3.2.117) -3 + 2 + -1 = -2

3.2.118) -5 + -3 + 2 + -1 = -7

3.2.119) 35 + -12 + 8 + -6 = 25

3.2.120) 20 + 15 + -3 + 6 = 38

3.2.121) -90 + 110 = 20

3.2.122) -168 + 140 = -28

3.2.123) -504 + 142 + -449 + 410 + 369 = -32

3.2.124) -201 + -16 + -23 + 172 + -34 = -102

3.2.125) you can model it out

 * -8 + 2 is ...
   
   ```
   pp
   nnnnnnnn
   ```

   there are 6 more negatives than there are positives, the answer is -6

 * 8 + -2 is ...

   ```
   pppppppp
   nn
   ```

   there are 6 more positives than there are negatives, the answer is 6

3.2.126) technical diving -- when you're 100 feet under water and you go down another 10 feet.. -100 + -10

## Chapter 3 Section 3

__TRY IT__

3.59)

```
pppppp 6

   ┌──────┐
pp │ pppp │ 6 - 4
   └──────┘
```

3.60)

```
ppppppp 7

    ┌──────┐
ppp │ pppp │ 7 - 4
    └──────┘
```

3.61)

```
nnnnnn 6

   ┌──────┐
nn │ nnnn │ 6 - 4
   └──────┘
```

3.62)

```
nnnnnnn 7

    ┌──────┐
nnn │ nnnn │ 7 - 4
    └──────┘
```

3.63)

```
nnnnnn -6
pppp 4

-6 - 4

no ps to subtract from the ns, so add an n for each p..

nnnnnn[nnnn]
       pppp

-10
```

3.64)

```
nnnnnnn -7
pppp 4

-7 - 4

no ps to subtract from the ns, so add an n for each p..

nnnnnnn[nnnn]
        pppp

-11
```

3.65)

```
pppppp 6
nnnn -4

no ns to subtract from the ps, so add a p for each n..

pppppp[pppp]
       nnnn

10
```

3.66)

```
ppppppp[pppp]
        nnnn

11
```

3.67)

* a)

  ```
  ppppppp[pppppppp]
          nnnnnnnn
  15
  ```

* b)

  ```
  nn[] -2
  nn   -2

  0
  ```

* c)

  ```
  ppp[pppp] 7
  ppp 3

  4
  ```

* d)

  ```
  nnnnnn[pp]
  nnnnnn nn

  2
  ```

3.68)

* a)

  ```
  pppp[pppppp]
       nnnnnn
  
  10
  ```

* b)

  ```
  [nnnnnnn]n

  -7
  ```

* c)

  ```
  [nnnnnnn]n

  -7
  ```

* d)
  
  ```
  nnnn[nn]
       pp
  
  6
  ```

3.69)

* a) 7 - 9

  ```
  ppppppp
  nnnnnnnnn <-- neutralize by adding 9 negatives, we have more negatives that positives
  
  -2
  ```

* b) -5 - (-9)

  ```
  nnnnn
  ppppppppp <-- neutralize by adding 10 positives, we have more positives than negatives
 
  4
  ```

3.70)

* a) 4 - 7

  ```
  pppp
  nnnnnnn  <-- neutralize by adding 9 negatives, we have more negatives than positives

  -3
  ```

* b) -7 - (-10)

  ```
  nnnnnnn
  pppppppppp <-- neutralize by adding 10 positives, we have more positives than negatives 
  
  3
  ```

3.71)

* a) 21 - 13 = 8, 21 + (-13) = 8
* b) -11 - 7 = -18, -11 + (-7) = -18

3.72)

* a) 15 - 7 = 8, 15 + (-7) = 8
* b) -14 - 8 = -22, -14 + (-8) = -22

3.73)

* a) 6 - (-13) = 19, 6 + 13 = 19
* b) -5 - (-1) = -4, -5 + 1 = -4

3.74)

* a) 4 - (-19) = 23, 4 + 19 = 23
* b) -4 - (-7) = 3, -4 + 7 = 3

3.75) -67 - (-38) = 29

3.76) -83 - (-57) = 26

3.77) 8 - (-3 - 1) - 9 = 8 - (-4) - 9 = 12 - 9 = 3

3.78) 12 - (-9 - 6) - 14 = 12 - (-15) - 14 = 27 - 14 = 13

3.79) 6(2) - 9(1) - 8(9) = 12 - 9 - 72 = 3 - 72 = -69

3.80) 2(5) - 3(7) - 4(9) = 10 - 21 - 36 = -11 - 36 = -47

3.81)

* a) 5 - 7 = -2
* b) -8 - 7 = -15

3.82)

* a) 1 - 3 = -2
* b) -4 - 3 = -7

3.83)

* a) 17 - 19 = -2
* b) 17 - -19 = 36

3.84)

* a) -5 - 14 = -19
* b) -5 - -14 = 9

3.85)

* a) 14 - -23 = 37
* b) -17 - 21 = -38

3.86)

* a) 11 - -19 = 30
* b) -11 - 18 = -29

3.87) 15 - -30 = 45

3.88) -5 - -16 = 11

3.89) 10023 - -80 = 10103

3.90) -340 - -573 = 233

3.91)

* a) 74 - 27 = 47
* b) 47 - 50 = -3
* c) -3 + 20 = 17

3.92)

* a) -78 + 24 = -54
* b) -54 + 49 = -5

__EXERCISE__

3.3.127) 8 - 2 = 6

```
pppppppp
nn

6 ps remaining
```

3.3.128) 9 - 3 = 6

```
ppppppppp
nnn

3 more ps remaining
```

3.3.129) -5 - -1 = -4

```
nnnn[n]

after removing 1 n, 4 ns remaining
```

3.3.130) -6 - -4

```
nn[nnnn]

after removing 4 n, 2 ns remaining
```

3.3.131) -5 - 4

```
nnnnnnnnn
     pppp

no ps to subtract from the ns, so add an n for each p.. 9 ns
```

3.3.132) -7 - 2

```
nnnnnnnnn
       pp

no ps to subtract from the ns, so add an n for each p.. 9 ns
```

3.3.133) 8 - -4

```
pppppppppppp
        nnnn

no ns to subtract from the ps, so add a p for each n.. 12 ps
```

3.3.134) 7 - (-3)

```
pppppppppp
       nnn

no ns to subtract from the ps, so add a p for each n.. 10 ps
```

3.3.135)

* a) 15 - 6 = 9
* b) 15 + -6 = 9

3.3.136)

* a) 12 - 9 = 3
* b) 12 + (-9) = 3

3.3.137)

* a) 44 - 28 = 16
* b) 44 + (-28) = 16

3.3.138)

* a) 35 - 16 = 19
* b) 35 + (-16) = 19

3.3.139)

* a) 8 - (-9) = 17
* b) 8 + 9 = 17

3.3.140)

* a) 4 - (-4) = 8
* b) 4 + 4 = 8

3.3.141)

* a) 27 - (-18) = 45
* b) 27 + 18 = 45

3.3.142)

* a) 46 - (-37) = 83
* b) 46 + 37 = 83

3.3.143) 15 - (-12) = 27

3.3.144) 14 - (-11) = 25

3.3.145) 10 - (-19) = 29

3.3.146) 11 - (-18) = 29

3.3.147) 48 - 87 = -39

3.3.148) 45 - 69 = -24

3.3.149) 31 - 79 = -48

3.3.150) 39 - 81 = -42

3.3.151) -31 - 11 = -42

3.3.152) -32 - 18 = -50

3.3.153) -17 - 42 = -59

3.3.154) -19 - 46 = -65

3.3.155) -103 - (-52) = -51

3.3.156) -105 - (-68) = -37

3.3.157) -45 - (-54) = 9

3.3.158) -58 - (-67) = -9

3.3.159) 8 - 3 - 7 = 5 - 7 = -2

3.3.160) 9 - 6 - 5 = 4 - 5 = -1

3.3.161) -5 - 4 + 7 = -9 + 7 = -2

3.3.162) -3 - 8 + 4 = -11 + 4 = -7

3.3.163) -14 - (-27) + 9 = 13 + 9 = 22

3.3.164) -15 - (-28) + 5 = 13  + 5 = 18

3.3.165) 71 + (-10) - 8 = 61 - 8 = 53

3.3.166) 64 + (-17) - 9 = 47 - 9 = 38

3.3.167) -16 - (-4 + 1) - 7 = -16 - (-3) - 7 = -13 - 7 = -20

3.3.168) -15 - (-6 + 4) - 3 = -15 - (-2) - 3 = -13 - 3 = -16

3.3.169) (2 - 7) - (3 - 8) = -5 - -5 = 0

3.3.170) (1 - 8) - (2 - 9) = -7 - -7 = 0

3.3.171) -(6 - 8) - (2 - 4) = -(-2) - (-2) = 2 - -2 = 4

3.3.172) -(4 - 5) - (7 - 8) = -(-1) - (-1) = 1 - (-1) = 2

3.3.173) 25 - [10 - (3 - 12)] = 25 - [10 - -9] = 25 - 19 = 6

3.3.174) 32 - [5 - (15 - 20)] = 32 - [5 - -5] = 32 - 10 = 42

3.3.175) 6.3 - 4.3 - 7.2 = 2 - 7.2 = -5.2 --- WHY ASK THIS? THE BOOK HASN'T COVERED DECIMAL NUMBERS YET

3.3.176) 5.7 - 8.2 - 4.9 = -2.5 - 4.9 = -7.4 --- WHY ASK THIS? THE BOOK HASN'T COVERED DECIMAL NUMBERS YET

3.3.177) 5^2 - 6^2 = 25 - 36 = -11

3.3.178) 6^2 - 7^2 = 36 - 49 = -13

3.3.179)

* a) 3 - 6 = -3
* b) 3 - -3 = 6

3.3.180)

* a) 5 - 4 = 1
* b) -5 - 4 = -9

3.3.181)

* a) 5 - 2 = 3
* b) 5 - -2 = 7

3.3.183) 4(3)^2 - 15(3) + 1 = 4(9) - 45 + 1 = 36 - 45 + 1 = -9 + 1 = -8

3.3.184) 5(2)^2 - 14(2) + 7 = 5(4) - 28 + 7 = 20 - 28 + 7 = -8 + 7 = -1

3.3.185) -12 - 5(6)^2 = -12 - 5(36) = -12 - 180 = -192

3.3.186) -19 - 4(5)^2 = -19 - 4(25) = -19 - 100 = -119

3.3.187)

* a) 3 - -10 = 13
* b) 45 - -20 = 65

3.3.188)

* a) 8 - -12 = 20
* b) 50 - -13 = 63

3.3.189)

* a) -6 - 9 = -15
* b) -16 - -12 = -4

3.3.190)

* a) -8 - 9 = -17
* b) -19 - -15 = -4

3.3.191)

* a) -17 - 8 = -25
* b) -24 - 37 = -61

3.3.192)

* a) -14 - 5 = -19
* b) -13 - 42 = -55

3.3.193)

* a) 6 - 21 = -15
* b) -19 - 31 = -50

3.3.194)

* a) 7 - 34 = -27
* b) -50 - 29 = -79

3.3.195) 28 - 38 = -10

3.3.196) 22 - 35 = -13

3.3.197) 84 - -12 = 96

3.3.198) 89 - -31 = 120

3.3.199) 30 + 2 - 7 - 4 = 21 

3.3.200) 20 - 8 + 5 - 6 = 11

3.3.201) 148 - 83 = 65

3.3.202) 426 - 152 = 274 

3.3.203) 210 - 250 = -40

3.3.204) 94 - 110 = -16

3.3.205) -14 + 40 = -26

3.3.206) -23 + 80 = -57

3.3.207) -20 - -7 = -13

3.3.208) -100 - -45 = -55

3.3.209) 9 to 0 is 9, 0 to -6 is 6 -- 9 + 6 is 15

3.3.210) when you subtract a negative, you go right on the number line by that amount -- you also go right on the number line when you add some amount.

## Chapter 3 Section 4

__TRY IT__

3.93) 

* a) -6 * 8 = -48
* b) -4 * -7 = 28
* c) 9 * -7 = -63
* d) 5 \* 12 = 60

3.94)

* a) -8 * 7 = -56
* b) -6(-9) = 54
* c) 7(-4) = -28
* d) 3 * 13 = 39

3.95)

* a) -1*9 = -9
* b) -1*-17 = 17

3.96)

* a) -1*8 = -8
* b) -1(-17) = 17

3.97)

* a) -42 / 6 = -7
* b) 117 / -3 = -39

3.98)

* a) -63 / 7 = -9
* b) -115 / -5 = 103

3.99)

* a) 6 / -1 = -6
* b) -36 / -1 = 36

3.100)

* a) 28 / -1 = -28
* b) -52 / -1 = 52

3.101)

* 8(-3) + 5(-7) - 4
* -24 + -35 - 4
* -59 - 4
* -63

3.102)

* 9(-3) + 7(-8) - 1
* -27 + -56 - 1
* -83 - 1
* -84

3.103)

* a) (-3)^4 = -3 \* -3 \* -3 \* -3 =  81
* b) -3^4 = -(3 \* 3 \* 3 \* 3) = -81

TODO: when you see something like -x^n, you evaluate it as -(x * x * x * ...). WHY? this of it as -1\*x^n -- do the exponent first than the multiplication.

3.104)

* a) (-7)^2 = -7 * -7 = 49
* b) -7^2 = -(7 * 7) = -49

3.105) 17 - 4(8 - 11) = 17 - 4(-3) = 17 - -12 = 29

3.106) 16 - 6(7 - 13) = 16 - 6(-6) = 16 - -36 = 52

3.107) 12(-9) / (-3)^2 = -108 / 9 = 12

3.108) 18(-4) / (-2)^3 = -72 / -8 = 9

3.109) -27 / 3 + (-5)(-6) = -27 / 3 + 30 = -9 + 30 = 21

3.110) -32 / 4 + (-2)(-7) = -32 / 4 + 14 = -16 + 14 = -2

3.111)

* 3(-3)^2 - 2(-3) + 6
* 3(9) - 2(-3) + 6
* 27 - -6 + 6
* 33 + 6
* 39

3.112)

* 4(-2)^2 - (-2) - 5
* 4(4) - (-2) - 5
* 16 - (-2) - 5
* 18 - 5
* 13

3.113)

* 7(-2) + 6(3) - 12
* -14 + 24 - 12
* 10 - 12
* -2

3.114)

* 8(-3) - 6(-5) + 13
* -24 - -30 + 13
* 6 + 13
* 19

3.115) -5 \* 12 = 60

3.116) 8 \* -13 = -104

3.117) -63 / -9 = 7

3.118) -72 / -9 = 8

__EXERCISE__

3.4.211) -4 * 8 = -32

3.4.212) -3 \* 9 = -27

3.4.213) -5(7) = -35

3.4.214) -8(6) = -48

3.4.215) -18(-2) = 36

3.4.216) -10(-6) = 60

3.4.217) 9(-7) = -63

3.4.218) 13(-5) = -65

3.4.219) -1(6) = -6

3.4.220) -1(3) = -3

3.4.221) -1(-14) = 14

3.4.222) -1(-19) = 19

3.4.223) -24 / 6 = -4

3.4.224) -28 / 7 = -4

3.4.225) 56 / -7 = -8

3.4.226) 35 / -7 = -5

3.4.227) -52 / -4 = 13

3.4.228) -84 / -6 = 14

3.4.229) -180 / 15 = -11

3.4.230) -192 / 12 = -16

3.4.231) 49 / -1 = -49

3.4.232) 62 / -1 = -62

3.4.233)

* 5(-6) + 7(-2) - 3
* -30 + 7(-2) - 3
* -30 + -14 - 3
* -44 - 3

3.4.234)

* 8(-4) + 5(-4) - 6
* -32 + -20 - 6
* -52 - 6
* -58

3.4.235)

* -8(-2) - 3(-9)
* 16 - 3(-9)
* 16 - -27
* 43

3.4.236)

* -7(-4) - 5(-3)
* 28 - 5(-3)
* 28 - -15
* 43

3.4.237)

* -5 \* -5 \* -5
* 25 \* -5
* -125

3.4.238)

* -4 \* -4 \* -4
* 16 \* -4
* -64

3.4.239)

* -2 \* -2 \* -2 \* -2 \* -2 \* -2
* 4 \* -2 \* -2 \* -2 \* -2
* -8 \* -2 \* -2 \* -2
* 16 \* -2 \* -2
* -32 \* -2
* 64

3.4.240)

* -3 \* -3 \* -3 \* -3 \* -3
* 9 \* -3 \* -3 \* -3
* -27 \* -3 \* -3
* 81 \* -3
* -243

3.4.241)

* -(4 * 4)
* -16

3.4.242)

* -(6 * 6)
* -36

3.4.243)

* -3(-5)(6)
* 15(6)
* 90

3.4.244)

* -4(-6)(3)
* 24(3)
* 72

3.4.245)

* -4 \* 2 \* 11
* -8 \* 11
* -88

3.4.246)

* -5 \* 3 \* 10
* -15 \* 10
* -150

3.4.247)

* (8 - 11)(9 - 12)
* (-3)(9 - 12)
* (-3)(-3)
* 9

3.4.248)

* (6 - 11)(8 - 13)
* (-5)(8 - 13)
* (-5)(-5)
* 25

3.4.249)

* 26 - 3(2 - 7)
* 26 - 3(-5)
* 26 - -15
* 41

3.4.250)

* 23 - 2(4 - 6)
* 23 - 2(-2)
* 23 - -4
* 27

3.4.251)

* -10(-4) / (-8)
* -40 / -8
* 5

3.4.252)

* -8(-6) / -4
* 48 / -4
* -12

3.4.253)

* 65 / (-5) + (-28) / (-7)
* -13 + (-28) / (-7)
* -13 + 4
* -9

3.4.254)

* 52 / (-4) + (-32) / (-8)
* -13 + 4
* -9

3.4.255)

* 9 - 2(3 - 8(-2))
* 9 - 2(3 - -16)
* 9 - 2(19)
* 9 - 38
* -29

3.4.256)

* 11 - 3(7 - 4(-2))
* 11 - 3(7 - -8)
* 11 - 3(15)
* 11 - 45
* -34

3.4.257)

* (-3)^2 - 24 / (8 - 2)
* 9 - 24 / (8 - 2)
* 9 - 24 / 6
* 9 - 4
* 5

3.4.258)

* (-4)^2 - 32 / (12 - 4)
* 16 - 32 / 8
* 16 - 4
* 12

3.4.259)

* a) -2(8) + 17 = -16 + 17 = -1
* b) -2(-8) + 17 = 16 + 17 = 33

3.4.260)

* a) -5(9) + 14 = -45 + 14 = -31 
* b) -5(-9) + 14 = 45 + 14 = 59

3.4.261)

* a) 10 - 3(5) = 10 - 15 = -5
* b) 10 - 3(-5) = 10 - -15 = 25

3.4.262)

* a) 18 - 4(3) = 18 - 12 = 6
* b) 18 - 4(-3) = 18 - -12 = 30

3.4.263)

* (-1)^2 - 5(-1) + 5
* 1 - -5 + 5
* 6 + 5
* 11

3.4.264)

* (-2)^2 - 2(-2) + 9
* 4 - -4 + 9
* 8 + 9
* 17

3.4.265)

* 2(-2)^2 - 3(-2) + 7
* 2(4) - 3(-2) + 7
* 8 - -6 + 7
* 14 + 7
* 21

3.4.266)

* 3(-3)^2 - 4(-3) + 5
* 3(9) - 4(-3) + 5
* 27 - -12 + 5
* 39 + 5
* 44

3.4.267)

* 6(3) - 5(-1) + 15
* 18 - 5(-1) + 15
* 18 - -5 + 15
* 23 + 15
* 38

3.4.268)

* 3(8) - 2(-2) + 9
* 24 - 2(-2) + 9
* 24 - -4 + 9
* 28 + 9
* 37

3.4.269)

* 9(-6) - 2(-3) - 8
* -54 - 2(-3) - 8
* -54 - -6 - 8
* -48 - 8
* -56

3.4.270)

* 7(-4) - 4(-9) - 2
* -28 - 4(-9) - 2
* -28 - -36 - 2
* 8 - 2
* 6

3.4.271) -3 * 5 = -15

3.4.272) -4 * 16 = -64

3.4.273) -60 / -20 = 3

3.4.274) -40  / - 20 = 2

3.4.275) -6 / (a + b)

3.4.276) -7 / (m + n)

3.4.277) -10 * (p - q)

3.4.278) -13 * (c - d)

3.4.279) (x - 12) * 300

3.4.280) (x - 3) * 8

3.4.281) if the signs are the same, the product has a positive sign. otherwise, product has negative sign

3.4.282) if the signs are the same, the quotient has a positive sign. otherwise, quotient has negative sign

3.4.283) you have to evaluate the exponent before the sign, because you have to think about -2 as -1 * 2, so the entire thing is really -1 * 2^4 because you evaluate exponents before multiplication

3.4.284) you have to evaluate the exponent before the sign, because you have to think about -4 as -1 * 4, so the entire thing is really -1 * 4^2 because you evaluate exponents before multiplication

## Chapter 3 Section 5

__TRY IT__

3.119) 2x - 8 = -14

* a) x=-11
  * 2(-11) - 8 = -14
  * -22 - 8 = -14
  * -30 = -14  (FALSE)
* b) x=11
  * 2(11) - 8 = -14
  * 22 - 8 = -14
  * 16 = -14 (FALSE)
* c) x=-3
  * 2(-3) - 8 = -14
  * -6 - 8 = -14
  * -14 = -14 (TRUE)

3.120) 2y + 3 = -11

* a) y=4
  * 2(4) + 3 = -11
  * 8 + 3 = -11
  * 11 = -11 (FALSE)
* b) y=-4
  * 2(-4) + 3 = -11
  * -8 + 3 = -11
  * -5 = -11 (FALSE)
* c) y=-7
  * 2(-7) + 3 = -11
  * -14 + 3 = -11
  * -11 = -11

3.121)
 * y + 11 = 7
 * (y + 11) - 11 = 7 - 11
 * y = -4

3.122)
 * y + 15 = -4
 * (y + 15) - 15 = -4 - 15
 * y = -19

3.123)
 * a - 2 = -8
 * (a - 2) + 2 = -8 + 2
 * a = -6

3.124)
 * n - 4 = -8
 * (n - 4) + 4 = -8 + 4
 * n = -4

3.125)

 * 4x = 12
 * 4x / 4 = 12 / 4
 * x = 3

3.126)

 * 3x = 6
 * 3x / 3 = 6 / 3
 * x = 2

3.127)

 * 8a = 56
 * 8a / 8 = 56 / 8
 * a = 7

3.128)

 * 11n = 121
 * 11n / 11 = 121 / 11
 * n  = 11

3.129)

 * -8p = 96
 * -8p / -8 = 96 / -8
 * p = -12

3.130)

 * -12m = 108
 * -12m / -12 = 108 / -12
 * m = -9

3.131)

 * 7 + x = -2
 * 7 + x - 7 = -2 - 7
 * x = -9

3.132)

 * 11 + y = 2
 * 11 + y - 11 = 2 - 11
 * y = -9

3.133)

 * p - 2 = -4
 * p - 2 + 2 = -4 + 2
 * p = -2

3.134)

 * q - 7 = -3
 * q - 7 + 7 = -3 + 7
 * q = 4

3.135)

 * -12 * y = 132
 * -12 * y / 12 = 132 / 12
 * y = 11

3.136)

 * -13 * x = 117
 * -13 * x / -13 = 117 / -13
 * x = -9

__EXERCISE__

3.5.285) 4x - 2 = 6

* a) x = -2
  * 4(-2) - 2 = 6
  * -8 - 2 = 6
  * -10 = 6 (FALSE)
* b) x = -1
  * 4(-1) - 2 = 6
  * -4 - 2 = 6
  * -6 = 6 (FALSE)
* c) x = 2
  * 4(2) - 2 = 6
  * 8 - 2 = 6
  * 6 = 6 (TRUE)

3.5.286) 4y - 10 = -14

* a) y = -6
  * 4(-6) - 10 = -14
  * -24 - 10 = -14
  * -34 = -14 (FALSE)
* b) y = -1
  * 4(-1) - 10 = -14
  * -4 - 10 = -14
  * -14 = -14 (TRUE)
* c) y = 1
  * 4(1) - 10 = -14
  * 4 - 10 = -14
  * -6 = -14 (FALSE)

3.5.287) 9a + 27 = -63

* a) a = 6
  * 9(6) + 27 = -63
  * 54 + 27 = -63
  * 81 = -63 (FALSE)
* b) a = -6
  * 9(-6) + 27 = -63
  * -54 + 27 = -63
  * -27 = -63 (FALSE)
* c) a = -10
  * 9(-10) + 27 = -63
  * -90 + 27 = -63
  * -63 = -63 (TRUE)

3.5.288) 7c + 42 = -56

* a) c = 2
  * 7(2) + 42 = -56
  * 14 + 42 = -56
  * 56 = -56 (FALSE)
* b) c = -2
  * 7(-2) + 42 = -56
  * -14 + 42 = -56
  * 28 = -56 (FALSE)
* c) c = -14
 * 7(-14) + 42 = -56
 * -98 + 42 = -56
 * -56 = -56 (TRUE)

3.5.289)

* n + 12 = 5
* n + 12 - 12 = 5 - 12
* n = -7

3.5.290)

* m + 16 = 2
* m + 16 - 16 = 2 - 16
* m = -14

3.5.291)

* p + 9 = -8
* p + 9 - 9 = -8 - 9
* p = -17

3.5.292)

* q + 5 = -6
* q + 5 - 5 = -6 - 5
* q = -12

3.5.293)

* u - 3 = -7
* u - 3 + 3 = -7 + 3
* u = -4

3.5.294)

* v - 7 = -8
* v - 7 + 7 = -8 + 7
* v = -1

3.5.295)

* h - 10 = -4
* h - 10 + 10 = -4 + 10
* h = 6

3.5.296)

* k - 9 = -5
* k - 9 + 9 = -5 + 9
* k = 4

3.5.297)

* x + (-2) = -18
* x + (-2) - (-2) = -18 - (-2)
* x = -16

3.5.298)

* y + (-3) = -10
* y + (-3) - (-3) = -10 - (-3)
* y = -7

3.5.299)

* r - (-5) = -9
* r - (-5) + (-5) = -9 + (-5)
* r = -14

3.5.300)

* s - (-2) = -11
* s - (-2) + (-2) = -11 + (-2)
* s = -13

3.5.301)

* 3x = 6
* 3x / 3 = 6 / 3
* x = 2

3.5.302)

* 2x = 10
* 2x / 2 = 10 / 2
* x = 5

3.5.303)

* 2x = 8
* 2x / 2 = 8 / 2
* x = 4

3.5.304)

* 3x = 9
* 3x / 3 = 9 / 3
* x = 3

3.5.305)

* 5x = 45
* 5x / 5 = 45 / 5
* x = 9

3.5.306)

* 4p = 64
* 4p / 4 = 64 / 4
* p = 16

3.5.307)

* -7c = 56
* -7c / -7 = 56 / -7
* c = -8

3.5.308)

* -9x = 54
* -9x / -9 = 54 / -9
* x = 6

3.5.309)

* -14p = -42
* -14p / -14 = -42 / -14
* p = 3

3.5.310)

* -8m = 40
* -8m / -8 = 40 / -8
* m = -5

3.5.311)

* -120 = 10q
* -120 / 10 = 10q / 10
* -12 = q

3.5.312)

* -75 = 15y
* -75 / 15 = 15y / 15
* -5 = y

3.5.313)

* 24x = 480
* 24x / 24 = 480 / 24
* x = 20

3.5.314)

* 18n = 540
* 18n / 18 = 540 / 18
* n = 30

3.5.315)

* -3z = 0
* -3z / -3 = 0 / -3
* z = 0

3.5.316)

* 4u = 0
* 4u / 4 = 0 / 4
* u = 0

3.5.317)

* 4 + n = 1
* 4 + n - 4 = 1 - 4
* n = -3

3.5.318)

* m + 9 = 5
* m + 9 - 9 = 5 - 9
* m = -4

3.5.319)

* 8 + p = -3
* 8 + p - 8 = -3 - 8
* p = -11

3.5.320)

* 2 + q = -7
* q = -7 - 2
* q = -9

3.5.321)

* a - 3 = -14
* a - 3 + 3 = -14 - 3
* a = -17

3.5.322)

* b - 5 = -2
* b - 5 + 5 = -2 + 5
* b = 3

3.5.323)

* -42 = -7x
* -42 / -7 = -7x / -7
* 6 = x

3.5.324)

* -54 = -9y
* -54 / -9 = -9y / -9
* 6 = y

3.5.325)

* -15f = 75
* -15f / -15 = 75 / -15
* f = -5

3.5.326)

* -18g = 36
* -18g / -18 = 36 / -18
* g = -2

3.5.327)

* -6 + c = 4
* -6 + c - -6 = 4 - -6
* c = 10

3.5.328)

* -2 + d = 1
* -2 + d + 2 = 1 + 2
* d = 3

3.5.329)

* n - 9 = -4
* n - 9 + 9 = -4 + 9
* n = 5

3.5.330)

* n - 13 = -10
* n - 13 + 13 = -10 + 13
* n = 3

3.5.331)

* a) x + 2 = 10, x = 8
* b) 2x = 10, x = 5

3.5.332)

* a) y + 6 = 12, y = 6
* b) 6y = 12, y = 2

3.5.333)

* a) -3p = 27, p = -9
* b) p - 3 = 27, p = 24

3.5.334)

* a) -2q = 34, q = -17
* b) q - 2 = 34, q = 36

3.5.335)

* a - 4 = 16
* a - 4 + 4 = 16 + 4
* a = 20

3.5.336)

* b - 1 = 11
* b - 1 + 1 = 11 + 1
* b = 12

3.5.337)

* -8m = -56
* -8m/-8 = -56/-8
*  m = 7

3.5.338) -6n = -48, n = -8

3.5.339) -39 = u + 13,  u = -52

3.5.340) -100 = v + 25, v = -125

3.5.341) 11r = -99, r = -9

3.5.342) 15s = -300, s = -20

3.5.343) 100 = 20d, d = 5

3.5.344) 250 = 25n, n = 10

3.5.345) -49 = x - 7, x = -42

3.5.346) 64 = y - 4, y = 68

3.5.347)

* 3c = 51
* 3c / 3 = 51 / 3
* c = 17

3.5.348)

* 4g = 24
* 4g / 4 = 24 / 4
* g = 6

3.4.349) sure -- it shows how the 15 needs to be grouped

3.4.350) 

for the first one ... 1 enevlope + 4 dots is the same as 12 dots

for the second one, 4 envelopes is the same as 12 dots

3.5.351) the multiple of -3 needs to be removed from the the x to isolate it -- adding 3 doesn't do that

3.5.352) 4y = 40, the multiple of 5 needs to be removed from teh y to isolate it -- subtracting 4 doesn't do that

## Chapter 4 Section 1

__TRY IT__

4.1)

* a) 3/8
* b) 4/9

4.2)

* a) 3/5
* b) 3/4

4.3) 6 slices of the 8 would be shaded -- it isn't easy to draw using text

4.4) 2 bars of the 5 would be shaded -- it isn't easy to draw using text

4.5) can't do fraction circles because drawing circles isn't easy using text

```
+-----+-----+-----+
| 1/3 | 1/3 | 1/3 |
+-----+-----+-----+
```

4.6) can't do fraction circles because drawing circles isn't easy using text

```
+-----+-----+-----+-----+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+-----+-----+-----+-----+
```

4.7) 1 2/3 (can't do fraction circles because drawing circles isn't easy using text)

4.8) 1 1 1/2 (can't do fraction circles because drawing circles isn't easy using text)

4.9) 5/3, 1 2/3

4.10) 13/8, 1 5/8

4.11)

```
+-----+-----+-----+-----+-----+-----+  +-----+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |  | 1/6 |
+-----+-----+-----+-----+-----+-----+  +-----+
```

4.12)

```
+-----+-----+-----+-----+-----+  +-----+
| 1/5 | 1/5 | 1/5 | 1/5 | 1/5 |  | 1/5 |
+-----+-----+-----+-----+-----+  +-----+
```

4.13)

```
+-----+-----+-----+-----+-----+-----+-----+  +-----+-----+
| 1/7 | 1/7 | 1/7 | 1/7 | 1/7 | 1/7 | 1/7 |  | 1/7 | 1/7 |
+-----+-----+-----+-----+-----+-----+-----+  +-----+-----+
```

1 2/7

4.14)

```
+-----+-----+-----+-----+ +-----+-----+-----+
| 1/4 | 1/4 | 1/4 | 1/4 | | 1/4 | 1/4 | 1/4 |
+-----+-----+-----+-----+ +-----+-----+-----+
```

1 3/4

4.15) 11/8

4.16) 11/6

4.17) 1 6/7

4.18) 1 5/9

4.19) 3 2/7

4.20) 4 4/11

4.21) 26/7

4.22) 23/8

4.23) 50/11

4.24) 34/3

4.25)

```
+-----------+-----------+-----------+-----------+
|    1/4    |    1/4    |    1/4    |    1/4    |
+-----+-----+-----+-----+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+-----+-----+-----+-----+
```

2/8 = 1/4

4.26)

```
+--------------------+--------------------+--------------------+--------------------+
|        1/4         |        1/4         |        1/4         |        1/4         |
+------+------+------+------+------+------+------+------+------+------+------+------+
| 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 |
+------+------+------+------+------+------+------+------+------+------+------+------+
```

3/12 = 1/4

4.27)

* 6/10
* 9/15
* 30/50

4.28)

* 40/50
* 8/10
* 20/25

4.29) 18/21

4.30) 30/100

4.31) can't do this using text

4.32) can't do this using text

4.33) can't do this using text

4.34) can't do this using text

4.35) 
* a) >
* b) >
* c) <
* d) <

4.36)
* a) >
* b) <
* c) >
* d) <

__EXERCISE__

4.1.1)

* a) 1/4
* b) 3/4
* c) 3/8
* d) 5/8

4.1.2)

* a) 7/12
* b) 5/12
* c) 4/9
* d) 5/9

4.1.3) 

```
+--------+
| filled |
+--------+
|        |
+--------+
```

4.1.4)

```
+--------+
| filled |
+--------+
|        |
+--------+
|        |
+--------+
```

4.1.5)

```
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
|        |
+--------+
```

4.1.6)

```
+--------+
| filled |
+--------+
| filled |
+--------+
|        |
+--------+
|        |
+--------+
|        |
+--------+
```

4.1.7)

```
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
|        |
+--------+
```

4.1.8)

```
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
|        |
+--------+
```

4.1.9)

```
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
|        |
+--------+
|        |
+--------+
|        |
+--------+
```

4.1.10)

```
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
| filled |
+--------+
|        |
+--------+
|        |
+--------+
|        |
+--------+
```

4.1.11) 1 1/2 (can't draw circles easily in text)

4.1.12) 1 (can't draw circles easily in text)

4.1.13) 1 1/6 (can't draw circles easily in text)

4.1.14) 1 1/3 (can't draw circles easily in text)

4.1.15) 1 2/5 (can't draw circles easily in text)

4.1.16) 1 3/4 (can't draw circles easily in text)

4.1.17)

* a) 5/4, 1 1/4
* b) 7/4, 1 3/4
* c) 11/8, 3/8

4.1.18)

* a) 9/8, 1 1/8
* b) 5/4, 1 1/4
* c) 11/9, 1 2/9

4.1.19)

* a) 11/4, 2 3/4
* b) 19/8, 2 3/8

4.1.20) 1 (can't draw circles easily in text)

4.1.21) 1 (can't draw circles easily in text)

4.1.22) 1 3/4 (can't draw circles easily in text)

4.1.23) 1 2/3 (can't draw circles easily in text)

4.1.24) 1 5/6 (can't draw circles easily in text)

4.1.25) 1 5/8 (can't draw circles easily in text)

4.1.26) 3 1/3 (can't draw circles easily in text)

4.1.27) 2 1/4 (can't draw circles easily in text)

4.1.28) 1 1/2

4.1.29) 1 2/3

4.1.30) 2 3/4

4.1.31) 2 3/5

4.1.32) 4 1/6

4.1.33) 3 1/9

4.1.34) 3 3/13

4.1.35) 3 2/15

4.1.36) 5/3

4.1.37) 7/5

4.1.38) 9/4

4.1.39) 17/6

4.1.40) 25/9

4.1.41) 19/5

4.1.42) 25/7

4.1.43) 32/9

4.1.44)

```
+-----------+-----------+-----------+
|    1/3    |    1/3    |    1/3    |
+-----+-----+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+-----+-----+
```

2/6

4.1.45)

```
+---------------------------+---------------------------+---------------------------+
|            1/3            |            1/3            |            1/3            |
+------+------+------+------+------+------+------+------+------+------+------+------+
| 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 |
+------+------+------+------+------+------+------+------+------+------+------+------+
```

4/12

4.1.46)

```
+-----------+-----------+-----------+-----------+
|    1/4    |    1/4    |    1/4    |    1/4    |
+-----+-----+-----+-----+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+-----+-----+-----+-----+
```

6/8

4.1.47)

```
+--------------------+--------------------+--------------------+--------------------+
|        1/4         |        1/4         |        1/4         |        1/4         |
+------+------+------+------+------+------+------+------+------+------+------+------+
| 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 |
+------+------+------+------+------+------+------+------+------+------+------+------+
```

9/12

4.1.48)

```
+-----------+-----------+-----------+
|    1/2    |    1/2    |    1/2    |
+-----+-----+-----+-----+-----+-----+
| 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 |
+-----+-----+-----+-----+-----+-----+
```

6/4

4.1.49)

```
+-----------------+-----------------+-----------------+
|       1/2       |       1/2       |       1/2       |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+
```

9/6

4.1.50)
* 1\*2 / 4\*2 = 2/8
* 1\*10 / 4\*10 = 10/40
* 1\*20 / 4\*20 = 20/80

4.1.51)
* 1\*2 / 3\*2 = 2/6
* 1\*10 / 3\*10 = 10/30
* 2\*20 / 3\*20 = 20/60

4.1.52)
* 3\*2 / 8\*2 = 6/16
* 3\*10 / 8\*10 = 30/80
* 3\*20 / 8\*20 = 60/160

4.1.53)
* 5\*2 / 6\*2 = 10/12
* 5\*10 / 6\*10 = 50/60
* 5\*20 / 6\*20 = 100/120

4.1.54)
* 2\*2 / 7\*2 = 4/14
* 2\*10 / 7\*10 = 20/70
* 2\*20 / 7\*20 = 40/140

4.1.55)
* 5\*2 / 9\*2 = 10/18
* 5\*10 / 9\*10 = 50/90
* 5\*20 / 9\*20 = 100/180

4.1.56) can't do this using text

4.1.57) can't do this using text

4.1.58) can't do this using text

4.1.59) can't do this using text

4.1.60) can't do this using text

4.1.61) can't do this using text

4.1.62) can't do this using text

4.1.63) can't do this using text

4.1.64) -1 < -1/4

4.1.65) -1 < -1/3

4.1.66) -2 1/2 > -3

4.1.67) -1 3/4 > -2

4.1.68) -5/12 > -7/12

4.1.69) -9/10 < -3/10

4.1.70) -3 < -13/5

4.1.71) -4 < -23/6

4.1.72) 1/5 count has 5 steps in a count, 1/4 count has 4 steps in a count

4.1.73)

* a) 2 measures
* b) 25/4, 6 1/4

4.1.74)

1/2 walnut per pan, 5 pans
* a) 2 1/2
* b) mixed number, because the baker probably has 1 cup and with mixed numbers its obvious how many whole cups are needed before going in for fractional portion

4.1.75) baking cookies

4.1.76) turn it into a mixed number, the dot dsits between the whole and the next number

so 21/4 = 5 1/4, the dot sits between 5 and 6 -- just past 5, it's a quarter of the way between 5 and 6

## Chapter 4 Section 2

__TRY IT__

4.37)
* 8/12
* 4/6
* 2/3

4.38)
* 12/16
* 6/8
* 3/4

4.39)
* -21/28
* -7/9

4.40)
* -16/24
* -4/6
* -2/3

4.41)
* -54/42
* -26/21

4.42)
* -81/45
* -9/5

4.43) 69 / 120

* 69
  * 3
  * 23

* 120
  * 10
    * 2
    * 5
  * 12
    * 3
    * 4

23 / 40

4.44) 120 / 192

* 120
  * 10
    * 2
    * 5
  * 12
    * 3
    * 4

* 192
  * 2
  * 96
    * 53
    * 2

60 / 96

4.45) 
* 7x/7y
* x/y

4.46)
* 9a/9b
* a/b

4.47)

```
                    cut here
                        |
                        v
+---------------+---------------+---------------+
|      1/5      |      1/5      |      1/5      |
+-------+-------+-------+-------+-------+-------+
| 1/10  | 1/10  | 1/10  | 1/10  | 1/10  | 1/10  |
+-------+-------+-------+-------+-------+-------+
```

3/10

4.48)

```
                                    cut here
                                        |
                                        v
+---------------+---------------+---------------+---------------+---------------+
|      1/6      |      1/6      |      1/6      |      1/6      |      1/6      |
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
| 1/12  | 1/12  | 1/12  | 1/12  | 1/12  | 1/12  | 1/12  | 1/12  | 1/12  | 1/12  |
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
```

5/12

4.49)
* 1/3 \* 2/5
* 1\*2/3\*5
* 2/15

4.50)
* 3/5 \* 7/8
* 3\*7/5\*8
* 21/40

4.51)
* -4/7 \* -5/8
* -4\*-5/7\*8
* 20/56

4.52)
* -7/12 \* -8/9
* -7\*-8/12\*9
* 56/108

4.53)
* -10/28 \* 8/15
* -10\*8/28\*15
* -80/420

4.54)
* -9/20 \* 5/12
* -9\*5/20\*12
* -45/240

4.55)
* a)
  * 1/8 \* 72/1
  * 1\*72/8\*1
  * 72/8
* b)
  * 11/3 \* -9a/1
  * 11\*-9a/3\*1
  * -99a/3

4.56)
* a)
  * 3/8 \* 64/1
  * 3\*64/8\*1
  * 192/8
* b)
  * 16x/1 \* 11/12
  * 16x\*11/1\*12
  * 176x/12

4.57)
* a) 5/7 -> 7/5
* b) -1/8 -> -8/1
* c) -11/4 -> -4/11
* d) 14 -> 1/14

4.58)
* a) 3/7 -> 7/3
* b) -1/12 -> -12/1
* c) -14/9 -> -9/14
* d) 21/1 -> 1/21

4.59)

| Number | Opposite | Absolute Value | Reciprocal |
| ------ | -------- | -------------- | ---------- |
| -5/8   | 5/8      | 5/8            | -8/5       |
| 1/4    | -1/4     | 1/4            | 4/1        |
| 8/3    | -8/3     | 8/3            | 3/8        |
| -8     | 8        | 8              | -1/8       |

4.60)

| Number | Opposite | Absolute Value | Reciprocal |
| ------ | -------- | -------------- | ---------- |
| -4/7   | 4/7      | 4/7            | -7/4       |
| 1/8    | -1/8     | 1/8            | 8/1        |
| 9/4    | -9/4     | 9/4            | 4/9        |
| -1     | 1        | 1              | -1         |

4.61) 1/3 / 1/6

how many 1/6s are there in 1/3?

1/3 can be re-written as 2/6

```
+---------------+
|      1/3      |
+-------+-------+
|  1/6  |  1/6  |
+-------+-------+
```

4.62)

```
+---------------+
|      1/2      |
+-------+-------+
|  1/4  |  1/4  |
+-------+-------+
```

4.63)

```
+-----------------------------------------------+
|                       2                       |
+-------+-------+-------+-------+-------+-------+
|  1/3  |  1/3  |  1/3  |  1/3  |  1/3  |  1/3  |
+-------+-------+-------+-------+-------+-------+
```

4.64)

```
+-----------------------------------------------+
|                       3                       |
+-------+-------+-------+-------+-------+-------+
|  1/2  |  1/2  |  1/2  |  1/2  |  1/2  |  1/2  |
+-------+-------+-------+-------+-------+-------+
```

4.65)

* 2/5 / -2/3
* 2/4 * -3/2
* -6/8
* -3/4

4.66)

* 2/3 /  -7/5
* 2/3 * -5/7
* -10/21

4.67)

* 3/5 / p/7
* 3/5 * 7/p
* 21/5p

4.68)

* 5/8 / q/3
* 5/8 * 3/q
* 15/8p

4.69)

* -2/3 / -5/6
* -2/3 * -6/5
* 12/15
* 4/5

4.70)

* -5/6 / -2/3
* -5/6 * -3/2
* 15/12
* 5/4

4.71)

* 7/27 / 35/36
* 7/27 * 36/35
* 252/945
* 84/315
* 28/105
* 4/15

4.72)

* 5/14 / 15/28
* 5/14 * 28/15
* 140/210
* 14/21
* 2/3

__EXERCISE__

4.2.77) 7/21 = 1/3

4.2.78) 8/24 = 1/3

4.2.79) 15/20 = 3/4

4.2.80) 12/18 = 6/9 = 2/3

4.2.81) -40/88 = -20/44 = -10/22 = -5/11

4.2.82) -63/99 = -21/33 = -7/11

4.2.83) -108/63 = -36/21 = -12/7

4.2.84) -104/48 = -52/24 = -26/12 = -13/6

4.2.85) 120/252 = 60/126 = 30/63 = 10/21

4.2.86) 182/294

* 182
  * 2
  * 91
    * 7
    * 13

* 294
  * 2
  * 147
    * 3
    * 49
      * 7
      * 7

common factors: 2, 7

182/294 = 91/147 = 13/21

4.2.87) -168/192 = -84/96 = -28/32 = -14/16 = -7/8

4.2.88) -140/224 = -70/112 = -10/16 = -5/8

4.2.89) 11x/11y = x/y 

4.2.90) 15a/15b = a/b

4.2.91) -3x/12y = -x/4y

4.2.92) -4x/32y = -x/8y

4.2.93) -14x^2/21y = -2x^2/3y

4.2.94) 24a/32b^2 = 12a/16b^2 = 6a/8b^2 = 3a/4b^2

4.2.95) 

```
   cut here
      |
      v
+-----+-----+
| 1/3 | 1/3 |
+-----+-----+
```

1/3

4.2.96)

```
                                cut here
                                   |
                                   v
+-------------+-------------+-------------+-------------+-------------+
|     1/8     |     1/8     |     1/8     |     1/8     |     1/8     |
+------+------+------+------+------+------+------+------+------+------+
| 1/16 | 1/16 | 1/16 | 1/16 | 1/16 | 1/16 | 1/16 | 1/16 | 1/16 | 1/16 |
+------+------+------+------+------+------+------+------+------+------+
```

5/16

4.2.97)

```
                  cut here
                     |
                     v
+-------------+-------------+-------------+-------------+-------------+
|     1/6     |     1/6     |     1/6     |     1/6     |     1/6     |
+------+------+------+------+------+------+------+------+------+------+
| 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 | 1/12 |
+------+------+------+------+------+------+------+------+------+------+
```

3/12

4.2.98)

```
           cut here
              |
              v
+--------------------+--------------------+
|        1/5         |        1/5         |
+------+------+------+------+------+------+
| 1/15 | 1/15 | 1/15 | 1/15 | 1/15 | 1/15 |
+------+------+------+------+------+------+
```

2/15

4.2.99) 2/15

4.2.100) 3/16

4.2.101) 27/40

4.2.102) 8/35

4.2.103) 6/24

4.2.104) 12/36 = 6/18 = 3/9 = 1/3

4.2.105) -15/90 = -3/18 = -1/6

4.2.106) 12/120 = 1/10

4.2.107) -56/252 = -28/126 = -14/63

4.2.108) -40/180 = -20/90 = -2/9

4.2.109) -126/300 = -63/150 = -21/50

4.2.110) -175/330 = -35/66

4.2.111) 2772/7560 = 1386/3780 = 693/1890 = 231/630 = 77/210 = 11/30 = 

4.2.112) 1320/5280 = 132/528 = 44/176 = 22/88 = 2/8 = 1/4

4.2.113) 20/11

4.2.114) 120/3 = 40/1

4.2.115) 63n/7 = 9n/1

4.2.116) 150m/6 = 75m/3 = 25m/1

4.2.117) 28p/4 = 14p/2 = 7p/1

4.2.118) 51q/3 = 17q/1

4.2.119) -136/4 = -68/2 = -34/1

4.2.120) -210/5 = -42/1

4.2.121) 3/8

4.2.122) 6/7

4.2.123) 8/21

4.2.124) 16/25

4.2.125) 1296/625  (cannot reduce any further, see factor trees for numerator and denominator below)

* 1296
  * 2
  * 648
    * 2
    * 324
      * 2
      * 162
        * 2
        * 81
          * 9
            * 3
            * 3
          * 9
            * 3
            * 3

* 625
  * 5
  * 125
    * 25
      * 5
      * 5
    * 5

4.2.126) 256/2401  (cannot reduce any further, see factor trees for numerator and denominator below)

* 256
  * 16
    * 4
      * 2
      * 2
    * 4
      * 2
      * 2
  * 16
    * 4
      * 2
      * 2
    * 4
      * 2
      * 2

* 2401
  * 7
  * 343
    * 7
    * 49
      * 7
      * 7
    
4.2.127) 4/3

4.2.128) 3/2

4.2.129) -17/5

4.2.130) -19/6

4.2.131) 11/8

4.2.132) -1/3

4.2.133)-1/19

4.2.134) -1/1

4.2.135) 1/1

4.2.136)

| Number | Opposite | Absolute Value | Reciprocal |
| ------ | -------- | -------------- | ---------- |
| -7/11  | 7/11     | 7/11           | -11/7      |
| 4/5    | -4/5     | 4/5            | 5/4        |
| 10/7   | -10/7    | 10/7           | 7/10       |
| -8     | 8        | 8              | -1/8       |

4.2.137)

| Number | Opposite | Absolute Value | Reciprocal |
| ------ | -------- | -------------- | ---------- |
| -3/13  | 3/13     | 3/13           | 13/3       |
| 9/14   | -9/14    | 9/14           | -14/9      |
| 15/7   | -15/7    | 15/7           | -7/15      |
| -9     | 9        | 9              | 1/9        |

4.2.138)

```
+-----------------------+
|          1/2          |
+-----------+-----------+
|    1/4    |    1/4    |
+-----------+-----------+
```

there are 2 instances of 1/4 in 1/2

4.2.139)

```
+-----------------------+
|          1/2          |
+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+
```

there are 4 instances of 1/8 in 1/2

4.2.140)

```
+-----------------------------------------------------------+
|                             10                            |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1/5 | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
```

there are 10 instances of 1/5 in 2

4.2.141)

```
+-----------------------------------------------------------------------+
|                                   3                                   | 
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
```

there are 12 instances of 1/4 in 3

4.2.142)

* 1/2 * 4/1
* 4/2
* 2/1

4.2.143)

* 1/2 * 8/1
* 8/2
* 4/1

4.2.144)

* 3/4 * 3/2
* 9/8

4.2.145)

* 4/5 * 4/3
* 20/15
* 4/3

4.2.146)

* -4/5 * 7/4
* -28/20
* -14/10
* -7/5

4.2.147)

* -3/4 * 5/3
* -15/12
* -5/4

4.2.148)

* -7/9 * -9/7
* 63/63
* 1/1

4.2.149)

* -5/6 * -6/5
* 30/30
* 1/1

4.2.150)

* 3/4 * 11/x
* 33/4x

4.2.151)

* 2/5 * 9/y
* 18/5y

4.2.152)

* 5/8 * 10/a
* 50/8a
* 25/4a

4.2.153)

* 5/6 * 15/c
* 75/6c

4.2.154)

* 5/18 * -24/25
* -120/450
* -12/45
* -4/9

4.2.155)

* 7/18 * -27/14
* -189/252
* -63/84
* -21/28
* -3/4

4.2.156)

* 7p/12 * 8/21p
* 56p/252p
* 56/252
* 28/126
* 14/63
* 2/9

4.2.157)

* 5q/12 * 8/15q
* 40q/180q
* 40/180
* 4/18
* 2/9

4.2.158)

* 8u/15 * 25/12v
* 200u/180v
* 20u/18v
* 10u/9v

4.2.159)

* 12r/25 * 35/18s
* 420r/450s
* 42r/45s
* 14r/15s

4.2.160)

* -5/1 * 2/1
* -10/1

4.2.161)

* -3/1 * 4/1
* -12/1

4.2.162)

* 3/4 * -1/12
* -3/48
* -1/19

4.2.163)

* 2/5 * -1/10
* -2/50
* -1/25

4.2.164)

* -18/1 * -2/9
* 36/9
* 4/1

4.2.165)

* -15/1 * -3/5
* 45/5
* 9/1

4.2.166)

* 1/2 * -4/3 * 8/7
* -32/21

4.2.167)

* 11/2 * 8/7 * 2/11
* 176/154
* 88/77
* 8/7

4.2.168)

* a) 3/4 * 2/1 = 6/4 = 3/2 = 1 1/2
* b)
  
  ```
  +-----------------+
  |       3/2       | 
  +-----+-----+-----+
  | 1/2 | 1/2 | 1/2 |
  +-----+-----+-----+
  ```

  ```
  +-----------------+
  |       3/2       | 
  +-----------+-----+
  |     1     | 1/2 |
  +-----------+-----+
  ```

4.2.169)

4 pan, 2/3 cups of condensed milk each

* a) 2/3 * 4/1 = 8/3 = 2 2/3
* b)
  
  ```
  +-----------------------------------------------+
  |                      8/3                      | 
  +-----+-----+-----+-----+-----+-----+-----+-----+
  | 1/3 | 1/3 | 1/3 | 1/3 | 1/3 | 1/3 | 1/3 | 1/3 |
  +-----+-----+-----+-----+-----+-----+-----+-----+
  ```

  ```
  +-----------------------------------------------+
  |                      8/3                      | 
  +-----------------+-----------------+-----+-----+
  |        1        |        1        | 1/3 | 1/3 |
  +-----------------+-----------------+-----+-----+
  ```

4.2.170)

* 5/1 / 1/4
* 5/1 * 4/1
* 20/1

4.2.171)

* 3/4 / 6/1
* 3/4 * 1/6
* 3/24
* 1/8

4.2.172) swap the num and denom

4.2.173) swap the num and denom

4.2.174) the number of slices doesn't matter as he would be getting the same amount of pizza either way

4.2.175) you have half a meter of ribbon remaining and you want to make sure that you only use 2/3rds of it -- that would be 1/3 meter 

## Chapter 4 Section 3

__TRY IT__

4.73)

* 17/3 * 6/17
* 102/51
* 34/17

4.74)

* 3/7 * 21/4
* 63/28
* 9/4

4.75)

* 40/7 * -21/8
* -840/56
* -420/28

4.76)

* -17/5 * 25/6
* -425/30
* -85/6

4.77)

* 35/8 / 7/1
* 35/8 * 1/7
* 35/56
* 5/8

4.78)

* 21/8 / 3/1
* 21/8 * 1/3
* 21/24
* 7/8

4.79)

* 8/3 / 4/3
* 8/3 * 3/4
* 24/12
* 2/1

4.80)

* 15/4 / 3/2
* 15/4 * 2/3
* 30/12
* 5/2

4.81) 9s/14

4.82) 5y/6

4.83) (a-b)/cd

4.84) (p+q)/r

4.85)

* 2/3 / 5/6
* 2/3 * 6/5
* 12/30
* 6/15
* 2/5

4.86)

* 3/7 / 6/11
* 3/7 * 11/6
* 33/42
* 11/14

4.87)

* -8/7 / 1/4
* -8/7 * 4/1
* -32/7

4.88)

* -3/1 / 9/10
* -3/1 * 10/9
* -30/9
* -10/3

4.89)

* a/8 / ab/6
* a/8 * 6/ab
* 6a/8ab
* 3a/4ab
* 3/4b

4.90)

* p/2 / pq/8
* p/2 * 8/pq
* 8p/2pq
* 4p/pq
* 4/q

4.91)

* 5/7 / 12/5
* 5/7 * 5/12
* 25/84

4.92)

* 8/5 / 16/5
* 8/5 * 5/16
* 8/16
* 1/2

4.93) -(3/5), 3/-5

4.94) -2/-7. 2/7

4.95) 10/8 = 5/4

4.96) -2/6 = -1/3

4.97) -9/12 = -3/4

4.98) -20/30 = -2/3

4.99) 16/72 = 8/36 = 4/18 = 2/9

4.100) 64/40 = 32/20 = 16/10 = 8/5

4.101) -28/7 = -4/1

4.102) -34/-17 = -2/1

__EXERCISE__

4.3.176)

* 35/8 * 7/10
* 245/80
* 49/16

4.3.177)

* 22/9 * 6/7
* 132/63
* 44/21

4.3.178)

* 15/22 * 18/5
* 270/110
* 27/11

4.3.179)

* 25/36 * 63/10
* 1575/360
* 315/72
* 105/36
* 35/13

4.3.180)

* 14/3 * -9/8
* -126/24
* -63/12
* -21/4

4.3.181)

* 12/5 * -20/9
* -240/45
* -48/9

4.3.182)

* -40/9 * 93/16
* -3720/144
* -310/12
* -155/6

4.3.183)

* -27/20 * 35/12
* -945/240
* -189/48
* -93/16

4.3.184)

* 16/3 * 1/4
* 16/12
* 4/3

4.3.185)

* 27/2 * 1/9
* 27/18
* 9/6
* 3/2

4.3.186)

* -12/1 * 11/36
* -132/36
* -66/18
* -33/9
* -11/3

4.3.187)

* -7/1 * 4/21
* -28/21
* -4/3

4.3.188)

* 51/8 / 8/17
* 51/17
* 3/1

4.3.189)

* 11/5 * 10/11
* 10/5
* 2/1

4.3.190)

* -48/5 * 5/-8
* 48/8
* 6/1

4.3.191)

* -75/4 * -4/15
* 75/15
* 5/1

4.3.192) 5u/11

4.3.193) 7v/13

4.3.194) p/q

4.3.195) a/b

4.3.196) r/s+10

4.3.197) a/3-b

4.3.198)

* 2/3 * 9/8
* 18/24
* 9/12
* 3/4

4.3.199)

* 4/5 * 15/8
* 60/40
* 6/4
* 3/2

4.3.200)

* -9/10 * 1/3
* -9/30
* -3/10

4.3.201)

* -9/16 * 40/33
* -360/108
* -180/54
* -90/27
* -30/9
* -10/3

4.3.202)

* -4/5 * 1/2
* -4/10
* -2/5

4.3.203)

* -9/10 * 1/3
* -9/30
* -3/10

4.3.204)

* 2/5 * 1/8
* 2/40
* 1/20

4.3.205)

* 5/3 * 1/10
* 5/30
* 1/8

4.3.206)

* m/3 * 2/n
* 2m/3n

4.3.207)

* r/5 * 3/s
* 3r/5s

4.3.208)

* x/6 * 9/8
* 9x/48
* 3x/16

4.3.209)

* 3/8 * 12/y
* 36/8y
* 18/4y
* 9/2y

4.3.210)

* 14/5 * 10/1
* 140/5
* 28/1

4.3.211)

* 14/3 * 6/1
* 84/3
* 28/1

4.3.212)

* 7/9 * -5/14
* -35/126
* -5/18

4.3.213)

* 3/8 * -4/27
* -12/216
* -4/72
* -2/34
* -1/17

4.3.214) (-5)/11, -5/11

4.3.215) (-4)/9, -4/9

4.3.216) (-11)/3, 11/(-3)

4.3.217) 13/(-6), (-13)/6

4.3.218) 15/8

4.3.219) 12/7

4.3.220) 25/10

4.3.221) 15/6

4.3.222)

* 48/9
* 19/3

4.3.223)

* 46/8
* 23/4

4.3.224) 0/12

4.3.225)

* -3/9
* -1/3

4.3.226)

* 8/6
* 4/3

4.3.227)

* 24/30
* 12/15
* 4/5

4.3.228)

* -40/10
* -4/1

4.3.229)

* -12/24
* -1/2

4.3.230)

* 12/12
* 1/1

4.3.231)

* 36/18
* 12/6
* 2/1

4.3.232)

* 15/25
* 3/5

4.3.233)

* 50/60
* 5/6

4.3.234)

* 34/17
* 2/1

4.3.235)

* 26/25

4.3.236)

* 50/20
* 5/2

4.3.237)

* 99/54
* 33/18
* 11/6

4.3.238)

* 28/14
* 2/1

4.3.239)

* 26/12
* 13/6

4.3.240)

* -16/2
* -8/1

4.3.241)

* -20/2
* -10/1

4.3.242)

* -14/7
* -2/1

4.3.243)

* 7+15/-11
* -22/9

4.3.244)

* (7\*4-2(8-5))/(9.3-3.5)
* (7\*4-2(8-5))/5.8
* (7\*4-2(3))/5.8
* (7\*4-6)/5.8
* (28-6)/5.8
* 22/5.8
* 220/58
* 110/29

why include questions with decimal numbers if you haven't discussed decimal numbers at all?

4.3.245)

* (9\*7-3(12-8))/(8.7-6.6)
* (9\*7-3(4))/2.1
* (9\*7-12)/2.1
* (63-12)/2.1
* -51/2.1
* -510/21
* -170/7

why include questions with decimal numbers if you haven't discussed decimal numbers at all?

4.3.246)

* 9(8-2) - 3(15-7) / 7(8-3) - 3(16-9)
* 9(6) - 3(8) / 7(5) - 3(7)
* 54 - 24 / 35 - 21
* 30 / 14
* 15 / 7

4.3.247)

* 8(9-2) - 4(14-9) / 7(8-3) - 3(16-9)
* 8(7) - 4(5) / 7(5) - 3(7)
* 56 - 20 / 35 - 21
* 36 / 14
* 18 / 7

4.3.248)

* a) 9/4 * 2/1 = 18/4 = 4 2/4 = 4 1/2
* b) 

  ```
  +-----+-----+-----+-----+-----+-----+-----+-----+-----+
  | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
  +-----+-----+-----+-----+-----+-----+-----+-----+-----+
  |           1           |           1           | 1/2 |
  +-----------------------+-----------------------+-----+
  ```

4.3.249)

* a) 1/2 * 8/3 = 8/6 = 4/3 = 1 1/3
* b) 10 * 8/3 = 80/3 = 26 2/3

4.3.250) swap the numerator and denominator

4.3.251) most straight forward way is to get both numbers as proper/improper fractions and multiply.

4.3.252) he's multiplying the wholes and then multiplying the fractions, which is not what you should be doing. convert both numbers into fractions first and then multiply.

4.3.253) fractions represent division, when only one of the operands into a division operation is negative, the result is negative

## Chapter 4 Section 4

__TRY IT__

4.103)

```
+-----+       +-----+-----+-----+-----+
| 1/8 |       | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+       +-----+-----+-----+-----+

combine to

+-----+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+-----+
```

4.104)

```
+-----+       +-----+-----+-----+-----+
| 1/6 |       | 1/6 | 1/6 | 1/6 | 1/6 |
+-----+       +-----+-----+-----+-----+

combine to

+-----+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+-----+
```

4.105) 5/6

4.106) 10/10

4.107) (x+3)/4

4.108) (y+5)/8

4.109) -15/d

4.110) -15/m

4.111) 9p/8

4.112) 9q/5

4.113) -10/15 = -2/3

4.114) -14/21 = -2/3

4.115) 3/8

4.116) 1/6

4.117) 12/28 = 6/14 = 3/7

4.118) 16/32 = 1/2

4.119) (x-2)/7

4.120) (y-13)/14

4.121) -2/x

4.122) -12/a

4.123) -5/5 = -1

4.124) -6/9 = -2/3

__EXERCISE__

4.4.254)

```
+-----+-----+      +-----+
| 1/5 | 1/5 |      | 1/5 |
+-----+-----+      +-----+

combine to

+-----+-----+-----+
| 1/5 | 1/5 | 1/5 |
+-----+-----+-----+
```

4.4.255)

```
+------+------+------+     +------+------+------+------+
| 1/10 | 1/10 | 1/10 |     | 1/10 | 1/10 | 1/10 | 1/10 |
+------+------+------+     +------+------+------+------+

combine to

+------+------+------+------+------+------+------+
| 1/10 | 1/10 | 1/10 | 1/10 | 1/10 | 1/10 | 1/10 |
+------+------+------+------+------+------+------+
```

4.4.256)

```
+-----+     +-----+-----+-----+
| 1/6 |     | 1/6 | 1/6 | 1/6 |
+-----+     +-----+-----+-----+

combine to

+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+
```

4.4.257)

```
+-----+-----+-----+     +-----+-----+-----+
| 1/8 | 1/8 | 1/8 |     | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+     +-----+-----+-----+

combine to

+-----+-----+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+-----+-----+
```

4.4.258) 5/9

4.4.259) 7/9

4.4.260) 13/13

4.4.261) 16/15

4.4.262) (x+3)/4

4.4.263) (y+2)/3

4.4.264) 16/p

4.4.265) 14/q

4.4.266) 11b/9

4.4.267) 9a/7

4.4.268) -9y/8

4.4.269) -4x/5

4.4.270) -4/8

4.4.271) -6/8

4.4.272) -10/16

4.4.273) -14/16

4.4.274) 7/17

4.4.275) 8/19

4.4.276) -16/13

4.4.277) -13/12

4.4.278)

```
+-----+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+-----+

slice off 

+-----+-----+
| 1/8 | 1/8 |
+-----+-----+

to become

+-----+-----+-----+
| 1/8 | 1/8 | 1/8 |
+-----+-----+-----+
```

4.4.279)

```
+-----+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+-----+

slice off 

+-----+-----+
| 1/6 | 1/6 |
+-----+-----+

to become

+-----+-----+-----+
| 1/6 | 1/6 | 1/6 |
+-----+-----+-----+
```

4.4.280) 3/5

4.4.281) 1/5

4.4.282) 4/15

4.4.283) 5/13

4.4.284) 6/12

4.4.285) 2/12

4.4.286) -15/21

4.4.287) -24/9

4.4.288) (y-9)/17

4.4.289) (x-8)/19

4.4.290) (5y-7)/8

4.4.291) (11z-8)/13

4.4.292) -5/d

4.4.293) -14/c

4.4.294) -38/u

4.4.295) -45/v

4.4.296) c/7

4.4.297) 3d/11

4.4.298) -9r/13

4.4.299) -14s/3

4.4.300) 1/5

4.4.301) 2/7 

4.4.302)-2/9

4.4.303) -3/11

4.4.304)

* -5/18 * 9/10
* -45/180
* -1/4

4.4.305)

* -3/14 * 7/12
* -21/168
* -1/8

4.4.306) (n-4)/5

4.4.307) (6-s)/11

4.4.308) -5/24

4.4.309) -4/18 = -2/9

4.4.310)

* 8/15 * 5/12
* 40/180
* 4/18
* 2/9

4.4.311)

* 7/12 * 28/9
* 196/108
* 98/54
* 49/27

4.4.312) 9/10

4.4.313) 2/8

4.4.314) 1/16, 1/8, 3/16, 1/4, 5/16, 8/8, 7/16, 1/2, 9/16, 5/8

4.4.315) no -- the number of slices is greater than 1 whole pizza

## Chapter 4 Section 5

__TRY IT__

4.125)

* 12
  * 3
  * 4
    * 2
    * 2

* 15
  * 5
  * 3

```
2 3 3
| 3 | 5
| | | |
v v v v
2 3 3 5 = 90
```

4.126)

* 15
  * 3
  * 5

* 5

```
3 5
| 5
| |
v v
3 5 = 15
```

4.127)

* 24
  * 4
    * 2
    * 2
  * 6
    * 3
    * 2

* 32
  * 16
    * 4
      * 2
      * 2
    * 4
      * 2
      * 2
  * 2

```
2 2 2     3
2 2 2 2 2 |
| | | | | |
v v v v v v
2 2 2 2 2 3 = 96
```

4.128)

* 28
  * 2
  * 14
    * 2
    * 7

* 32
  * 16
    * 4
      * 2
      * 2
    * 4
      * 2
      * 2
  * 2

```
2 2       7
2 2 2 2 2 |
| | | | | |
v v v v v v
2 2 2 2 2 7 = 224
```

4.129)

* 12 / 4 = 3 (multiplier for 3/4)
* 12 / 6 = 2 (multiplier for 5/6)

9/12, 10,12

4.130)

* 60 / 12 = 5 (multiplier for -7/12)
* 60 / 15 = 4 (multiplier for 11/15)

-35/60, 44/60

4.131) 

* 96 / 24 = 4
* 96 / 32 = 3

52/96, 51/96

4.132)

* 224 / 28 = 8
* 224 / 32 = 7

72/224, 189/224

4.133) 3/12 + 4/12 = 7/12

4.134) 5/10 + 2/10 = 7/10

4.135) 4/8 - -1/8 = 5/8

4.136) 2/6 - -1/6 = 3/6

4.137)

* 12
  * 3
  * 4
    * 2
    * 2

* 15
  * 3
  * 5

```
2 2 3  
| | 3 5
| | | |
v v v v
2 2 3 5 = 60

60/12=5
60/15=4
```

* 7/12 * 5/5 = 35/60
* 11/15 * 4/4 = 44/60

35/60 + 44/60 = 79/60

4.138)

* 15
  * 3
  * 5

* 20
  * 5
  * 4
    * 2
    * 2

```
    3 5
2 2 | 5
| | | |
v v v v
2 2 3 5 = 60

60/15 = 4
60/20 = 3
```

* 13/15 * 4/4 = 52/60
* 17/20 * 3/3 = 51/60

52/60 + 51/60 = 103/60

4.139) 13/24 - 17/32

* 24
  * 6
    * 3
    * 2
  * 4
    * 2
    * 2

* 32
  * 8
    * 4
      * 2
      * 2
    * 2
  * 4
    * 2
    * 2

```
      +-+-- 2*2 missing
      | |
      v v
2 2 2     3
2 2 2 2 2
          ^
          |
          +-- 3 missing
```

* 13/24 * 4/4 = 52/96
* 17/32 * 3/3 = 51/96

52/96 - 51/96 = 1/96

4.140) 21/32 - 9/28

* 32
  * 4
    * 2
    * 2
  * 8
    * 4
      * 2
      * 2
    * 2

* 28
  * 2
  * 14
    * 2
    * 7

```
          +-- 7 missing
          |
          v
2 2 2 2 2
2 2       7
    ^ ^ ^
    | | |
    +-+-+-- 2*2*2 missing
```

* 21/32 * 7/7 = 147/224
* 9/28 * 8/8 = 72/224

147/224 - 72/224 = 75/224

4.141) -13/42 + 17/35

* 42
  * 2
  * 21
    * 3
    * 7

* 35
  * 5
  * 7

```
    +-- missing 5
    |
    v
2 3   7
    5 7
^ ^
| |
+-+-- 2 * 3 missing
```

* -13/42 * 5/5 = -65/210
* 17/35 * 6/6 = 102/210

-65/210 + 102/210 = 37/210

4.142) -19/24 + 17/32

* 24
  * 6
    * 3
    * 2
  * 4
    * 2
    * 2

* 32
  * 8
    * 4
      * 2
      * 2
    * 2
  * 4
    * 2
    * 2

```
      +-+-- 2*2 missing
      | |
      v v
2 2 2     3
2 2 2 2 2  
          ^
          |
          +-- 3 missing
```

* -19/24 * 4/4 = -76/96
* 17/32 * 3/3 = 51/96

-76/96 + 51/96 = -25/96

4.143) y/6 + 7/9

* 6
  * 2
  * 3

* 9
  * 3
  * 3

```
  +-- 3 missing
  |
  v
2   3
  3 3
^
|
+-- 2 missing
```

y/6 * 3/3 = 3y/18
7/9 * 2/2 = 14/18

3y/18 + 14/18 = (3y + 14)/18

4.144) x/6 + 7/15

* 6
  * 2
  * 3

* 15
  * 3
  * 5

```
    +-- 5 missing
    |
    v
2 3
  3 5
^
|
+-- 2 missing
```

x/6 * 5/5 = 5x/30
7/15 * 2/2 = 14/30

5x/30 + 14/30 = (5x+14)/30

4.145)

* a) -9/12 - 2/12 = -11/12
* b) -1/4 * 6/1 = -6/4 = -3/2

4.146)

* a) 5/6 * -4/1 = -20/6 = -10/4 = -5/2
* b) 10/12 - 3/12 = 7/12

4.147)

* a) 3a/4 - 8/9 = 24a/36 - 32/36 = (24a - 32)/36 = 8(3a - 4)/36 = 4(3a - 4)/18  = 2(3a-4)/9
* b) 3a/4 \* 8/9 = 18a/36 = 2a/4 = a/2

4.148)

* a) 4k/5 + 5/6 = 20k/30 + 25/30 = (20k + 25)/30 = 5(4k+5)/30 = (4k+5)/6
* b) 4k/5 * 6/5 = 24k/25

4.149)

* (1/9) / (10/1)
* 1/9 * 1/10
* 1/90

4.150)

* (17/1) / (1/16)
* 17/1 * 16/1
* 272/1

4.151)

* (1/3 + 1/2) / (3/4 - 1/3)
* (2/6 + 3/6) / (3/4 - 1/3)
* (5/6) / (9/12 - 4/12)
* (5/6) / (5/12)
* 5/6 * 12/5
* 60/30
* 2/1

4.152)

* (2/3 - 1/2) / (1/4 + 1/3)
* (4/6 - 3/6) / (3/12 + 4/12)
* (1/6) / (7/12)
* 1/6 * 12/7
* 12/42
* 6/21
* 2/7

4.153)

* a) -7/4 + 3/4 = -4/4
* b) -5/4 + 3/4 = -2/4

4.154)

* a) 2/3 + 1/2 = 4/6 + 3/6 = 7/6
* b) -3/4 + 1/2 = -3/4 + 2/4 = -1/4

4.155) -1/4 - 1/2 = -1/4 - 2/4 = -3/4

4.156) -5/2 - 3/8 = -20/8 - 3/8 = -23/8

4.157)

* 3(-2/3)(-1/2)^2
* 3(-2/3)(1/4)
* 3(-2/12)
* (3/1)(-2/12)
* -6/12

4.158)

* 4((-1/2)^3)(-4/3)
* 4(-1/8)(-4/3)
* 4(4/24)
* (4/1)(4/24)
* 16/24

4.159)

* (-8 + -7)/6
* -15/6

4.160)

* (9+-18)/-6
* -9/-6
* 9/6
* 3/2

__EXERCISE__

4.5.316) 12

4.5.317) 20

4.5.318) 24

4.5.319) 48

4.5.320) 210

```
2 3 5
2 3   7
```

4.5.321) 240

```
2       3 5
2 2 2 2 3
```

4.5.322) 280

```
      5 7
2 2 2   7
```

4.5.323) 245

```
5 7
  7 7
```

4.5.324) 12

```
    3
  2 3
2 2
```

4.5.325) 60

```
    3
2 2
      5
```

4.5.326) 4/12, 3/12

4.5.327) 5/20, 4/20

4.5.328) 10/24, 21/24

4.5.329) 14/24, 15/24

4.5.330) 39/48, -44/48

4.5.331) 33/48, -20/48

4.5.332) 3/12, 10/12, 9/12

4.5.333) 20/60, 45/60, 36/60

4.5.334) 8/15

4.5.335) 9/20

4.5.336) 9/14

4.5.337) 11/24

4.5.338) 4/9

4.5.339) 3/8

4.5.340) 3/10

4.5.341) 4/6 = 2/3

4.5.342) 8/12 + 9/12 = 17/12

4.5.343) 15/20 + 8/20 = 23/20

4.5.344) 14/24 + 15/24 = 29/24

4.5.345) 10/24 + 9/24 = 19/24

4.5.346) 7/12 - 9/16

* 12
  * 3
  * 4
    * 2
    * 2

* 16
  * 4
    * 2
    * 2
  * 4
    * 2
    * 2

```
    +-+-- 2*2 missing
    | |
    v v
2 2     3
2 2 2 2
        ^
        |
        +-- 3 missing
```

(7/12 * 4/4) - (9/16 * 3/3) = 28/36 - 27/36 = 1/36

4.5.347) (7/16 * 3/3) - (5/12 * 4/4) = 21/36 - 20/36 = 1/36

4.5.348) 22/24 - 9/24 = 13/24

4.5.349) 15/24 - 14/24 = 1/24

4.5.350) 16/24 - 9/24 = 7/24

4.5.351) 10/12 - 9/12 = 1/12

4.5.352) -11/120 + 81/120 = 70/120 = 7/12

4.5.353) -27/60 + 34/60 = -7/60

4.5.354) -13/30 + 25/42 = 

* 30
  * 3
  * 10
    * 2
    * 5

* 42
  * 21
    * 3
    * 7
  * 2

```
      +-- 7 missing
      |
      v
2 3 5
2 3   7
    ^
    |
    +-- 5 missing
```

(-13/30 * 7/7) + (25/42 * 5/5) = -91/210 + 125/210

4.5.355) -23/30 + 5/48

* 30
  * 3
  * 10
    * 2
    * 5

* 48
  * 2
  * 24
    * 4
      * 2
      * 2
    * 6
      * 2
      * 3

```
  +-+-+-- 2*2*2 missing
  | | |
  v v v
2       3 5 
2 2 2 2 3
          ^
          |
          +-- 5 missing
```

(-23/30 * 8/8) + (5/48 * 5/5) = -184/240 + 25/240 = -159/240 = -53/80

4.5.356) -39/56 - 22/35

* 56
  * 7
  * 8
    * 4
      * 2
      * 2
    * 2

* 35
  * 5
  * 7

```
      +-- 5 missing
      |
      v
2 2 2   7
      5 7
^ ^ ^
| | |
+-+-+-- 2*2*2 missing
```

(-39/56 * 5/5) - (22/35 * 8/8) = -195/280 - 176/280 = -371/280 = 53/40

4.5.357) -33/49 - 18/35

* 49
  * 7
  * 7

* 35
  * 5
  * 7

```
+-- 5 missing
|
v
  7 7
5 7
    ^
    |
    +-- 7 missing
```

(-33/49 * 5/5) - (18/35 * 7/7) = (-165/245) - (126/245) = -291/245

4.5.358) -8/12 - (-9/12) = 1/12

4.5.359) -15/20 - (-16/20) = 1/20

4.5.360) -45/80 - (-64/80) = 19/80

4.5.361) -14/40 - (-25/40) = 11/40

4.5.362) 8/8 + 7/8 = 15/8

4.5.363) 6/6 + 5/6 = 11/6

4.5.364) 9/9 - 5/9 = 4/9

4.5.365) 10/10 - 3/10 = 7/10

4.5.366) x/3 + 1/4 = 4x/12 + 3/12 = (4x+3)/12

4.5.367) y/2 + 2/3 = 3y/6 + 4/6 = (3y+4)/6

4.5.368) y/4 - 3/5 = 5y/20 - 12/20 = (5y-12)/20

4.5.369) x/5 - 1/4 = 4x/20 - 5/20 = (4x-5)/20

4.5.370)

* a) 3/4 + 1/6 = 9/12 + 2/12 = 11/12
* b) 3/4 * 6/1 = 18/4 = 9/2

4.5.371)

* a) 4/6 + 1/6 = 5/6
* b) 2/3 * 6/1 = 12/3 = 4/1

4.5.372)

* a) -2/5 - 1/8 = -8/40 - 4/40 = -12/40 = -6/20 = -3/10
* b) -2/5 * 1/8 = -2/40 = -1/20

4.5.373)

* a) -4/5 - 1/8 = -32/40 - 5/40 = -37/40
* b) -4/5 * 1/8 = -4/40 = -1/10

4.5.374)

* a) 5n/6 * 15/8 = 75n/48 = 25n/19
* b) 5n/6 - 8/15 = 25n/30 - 16/30 = (25n-16)/30

4.5.375)

* a) 3a/8 * 12/7 = 36a/56 = 18a/28 = 9a/14
* b) 3a/8 - 7/12 = 21a/48 = 7a/16

4.5.376)

* a) 9/10 * -11d/12 = 99d/120
* b) 9/10 + -11d/12 = (9/10 * 6/6) + (-11d/12 * 5/5) = 54/60 + -55d/60 = (54 + -55d)/60

4.5.377)

* a) 4/15 * -5/q = -20/15q = -4/3q
* b) 4/15 + -5/q = (4/15 * q/q) + (-5/q * 15/15) = 4q/15q + -75/15q = (4q-75)/15q

4.5.378) -3/8 * -10/3 = 30/24 = 15/12

4.5.379) -5/12 * -9/5 = 9/12

4.5.380) -3/8 + 5/12 = (-3/8 * 3/3) + (5/12 * 2/2) = -9/24 + 10/24 = 1/24

4.5.381) -1/8 + 7/12 = (-1/8 * 3/3) + (7/12 * 2/2) = -3/24 + 14/24 = 11/24

4.5.382) 5/6 - 1/9 = (5/6 * 3/3) - (1/9 * 2/2) = 15/18 - 2/18 = 13/18

4.5.383) 5/9 - 1/6 = (5/9 * 2/2) - (1/6 * 3/3) = 10/18 - 3/18 = 7/18

4.5.384) 3/8 * -10/21 = -30/168 = -15/84 = -5/28

4.5.385) 7/12 * -8/35 = -56/420 = -28/210 = -14/105 = -2/15

4.5.386) -7/15 - y/4 = (-7/15 * 4/4) - (y/4 * 15/15) = -28/60 - 15y/60 = (-28 - 15y)/60

4.5.387) -3/8 - x/11 = (-3/8 * 11/11) - (x/11 * 8/8) = -33/88 - 8x/88 = (-33 - 8x)/88

4.5.388) 11/12a * 9a/16 = 99a/192a = 33a/64a = 33/64

4.5.389) 10y/13 * 8/5y = 80y/65y = 16y/13y = 16/13

4.5.390)

* 1/25 / 11/1
* 1/25 * 1/11
* 1/275

4.5.391)

* 1/9 / 9/1
* 1

4.5.392)

* 24/1 / 4/9
* 24/1 * 9/4
* 216 / 4
* 108 / 2
* 54 / 1

4.5.393)

* 21/1 / 9/16
* 21/1 * 16/9
* 336/9
* 112/3

4.5.394)

* 9/25 / 9/49
* 9/25 * 49/9
* 49/25

4.5.395)

* 9/16 / 25/64
* 9/16 * 64/25
* 576/400
* 288/200
* 144/100
* 72/50
* 36/25

4.5.396)

* 2/1 / (1/3 + 1/5)
* 2/1 / (5/15 + 3/15)
* 2/1 / 8/15
* 2/1 * 15/8
* 30/8
* 15/4

4.5.397)

* 5/1 / (1/4 + 1/3)
* 5/1 / (3/12 + 4/12)
* 5/1 / 7/12
* 5/1 * 12/7
* 60/7

4.5.398)

* (2/3 + 1/2) / (3/4 - 2/3)
* (4/6 + 3/6) / (9/12 - 8/12)
* 7/6 / 1/12
* 7/6 * 12/1
* 84/6
* 42/3
* 14/1

4.5.399)

* (3/4 + 1/2) / (3/4 - 2/3)
* (3/4 + 2/4) / (9/12 - 8/12)
* 5/4 / 1/12
* 5/4 * 12/1
* 60/4
* 30/2
* 15/1

4.5.400)

* (7/8 - 2/3) / (1/2 + 3/8)
* (21/24 - 16/24) / (4/8 + 3/8)
* 5/24 / 7/8
* 5/24 * 8/7
* 40/168
* 20/84
* 10/42
* 5/21

4.5.401)

* (3/4 - 3/5) / (1/4 + 2/5)
* (15/20 - 12/20) / (5/20 + 10/20) 
* 3/20 / 15/20
* 3/20 * 20/15
* 3/15
* 1/5

4.5.402)

* 1/2 + (2/3 * 5/12)
* 1/2 + (10/36)
* 1/2 + (10/36)
* 18/36 + 10/36
* 28/36

4.5.403)

* 1/3 + 2/5 * 3/4
* 1/3 + 6/20
* 20/60 + 18/60
* 38/60
* 19/30

4.5.404)

* 1 - 3/5 / 1/10
* 1 - 3/5 * 10/1
* 1 - 30/5
* 5/5 - 30/5
* -25/5
* -5/1

4.5.405)

* 1 - 5/6 / 1/12
* 1 - 5/6 * 12/1
* 1 - 60/6
* 1 - 10/1
* -9

4.5.406)

* 2/3 + 1/6 + 3/4
* 4/6 + 1/6 + 3/4
* 5/6 + 3/4
* 10/12 + 9/12
* 19/12

4.5.407)

* 2/3 + 1/4 + 3/5
* 2/3 + 5/20 + 12/20
* 2/3 + 17/20
* 40/60 + 51/60
* 91/60

4.5.408)

* 3/8 - 1/6 + 3/4
* 3/8 - 2/12 + 9/12
* 3/8 - 11/12
* 3/8 - 11/12
* 9/24 - 22/24
* -13/24

4.5.409)

* 2/5 + 5/8 - 3/4
* 2/5 + 5/8 - 6/8
* 2/5 + -1/8
* 16/40 + -5/40
* 11/40

4.5.410)

* 12/1 * (9/20 - 4/15)
* 12/1 * (27/60 - 16/60)
* 12/1 * (27/60 - 16/60)
* 12/1 * 11/60
* 132/60
* 66/30
* 33/15
* 11/5

4.5.411)

* 8/1 * (15/16 - 5/6)
* 8/1 * (90/96 - 80/96)
* 8/1 * 10/96
* 80/96
* 40/48
* 20/24
* 10/12
* 5/6

4.5.412)

* (5/8 + 1/6) / 19/24
* (15/24 + 4/24) / 19/24
* 19/24 / 19/24
* 1

4.5.413)

* (1/6 + 3/10) / 14/30
* (5/30 + 9/30) / 14/30
* 14/30 / 14/30
* 1

4.5.414)

* (5/9 + 1/6) / (2/3 - 1/2)
* (5/9 + 1/6) / (4/6 - 3/6)
* (25/45 + 9/45) / (4/6 - 3/6)
* 34/45 / 1/6
* 34/45 * 6/1
* 204/45

4.5.415)

* (3/4 + 1/6) / (5/8 - 1/3)
* (18/24 + 4/24) / (5/8 - 1/3)
* 22/24 / (5/8 - 1/3)
* 22/24 / (15/24 - 8/24)
* 22/24 / 7/24
* 22/24 * 24/7
* 22/7

4.5.416)

* a) -1/8 + 1/2 = -1/8 + 4/8 = 3/8
* b) -1/2 + 1/2 = 0

4.5.417)

* a) -1/6 + 2/3 = -1/6 + 4/6 = 3/6 = 1/2
* b) -5/3 + 2/3 = -3/3 = -1

4.5.418)

* a) 1/3 + (-5/6) = 2/6 + -5/6 = -3/6 = -1/2
* b) -1/6 + (-5/6) = -6/6 = -1

4.5.419)

* a) 11/12 + -11/12 = 0/12
* b) 3/4 + -11/12 = 9/12 + -11/12 = -2/12 = -1/6

4.5.420)

* a) 3/5 - 2/5 = 1/5
* b) -3/5 - 2/5 = -5/5 = -1

4.5.421)

* a) 2/3 - 1/3 = 1/3
* b) -2/3 - 1/3 = -3/3 = -1

4.5.422)

* a) 7/10 - 1/2 = 7/10 - 5/10 = 2/10 = 1/5
* b) 7/10 - -1/2 = 7/10 - -5/10 = 12/10 = 6/5

4.5.423)

* a) 5/12 - 1/4 = 5/12 - 3/12 = 2/12 = 1/6
* b) 5/12 - -1/4 = 5/12 - -3/12 = 8/12 = 4/6 = 2/3

4.5.424)

* 4/1 * (-1/2)^2 * 5/9
* 4/1 * 1/4 * 5/9
* 4/4 * 5/9
* 5/9

4.5.425)

* 5/1 * (-2/5)^2 * 1/3
* 5/1 * 4/10 * 1/3
* 20/10 * 1/3
* 2/1 * 1/3
* 2/3

4.5.426)

* 2/1 * (-2/3)^2 * (-1/2)^3
* 2/1 * 4/9 * -1/8
* 2/1 * 4/9 * -1/8
* 8/9 * -1/8
* -1/9

4.5.427)

* 8/1 * (-3/4)^2 * (-1/2)^3
* 8/1 * 9/16 * -1/8
* 8/1 * -1/8 * 9/16
* -1/1 * 9/16
* -9/16

4.5.428)

* (-4 + -8) / 2
* -12 / 2
* -6

4.5.429)

* (-6 + -2) / 4
* -8 / 4
* -2

4.5.430)

* (-3 + 8) / (-3 - 8)
* 5 / -11
* -5/11

4.5.431)

* (10 - -5) / (10 + -5)
* 15 / 5
* 3/1

4.5.432) 3/16 + 3/8 = 3/16 + 6/16 = 9/16

4.5.433) 5/4 + 9/8 = 10/8 + 9/8 = 19/8

4.5.434) the pieces being added or subtracted need to be of equal size

4.5.435) list out the prime factors in each denom -- the missing elements is what you need to multiply each denom by to get them both to equal the lcd 

## Chapter 4 Section 6

__TRY IT__

4.161)

```
+-----------------------------+
|                             |
+-----------------------------+
+-----+-----+
| 1/5 | 1/5 |
+-----+-----+


--------------------------------------------------------------


+-----------------------------+
|                             |
+-----------------------------+
+-----------------------------+
|                             |
+-----------------------------+
+-----------------------------+
|                             |
+-----------------------------+
+-----+-----+-----+
| 1/5 | 1/5 | 1/5 |
+-----+-----+-----+
```

5


4.162)

```
+-----------------------------------+
|                                   |
+-----------------------------------+
+-----------------------------------+
|                                   |
+-----------------------------------+
+-----+
| 1/6 |
+-----+


--------------------------------------------------------------


+-----------------------------------+
|                                   |
+-----------------------------------+
+-----------------------------------+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |
+-----------------------------------+
+-----+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+-----+
```

5

4.163)

```
+-----------------------------------+
|                                   |
+-----------------------------------+
+-----------------------------------+
|                                   |
+-----------------------------------+
+-----------------------------------+
|                                   |
+-----------------------------------+
+-----------------------------------+
|                                   |
+-----------------------------------+
+-----+-----+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+-----+-----+
+-----+-----+-----+-----+
| 1/6 | 1/6 | 1/6 | 1/6 |
+-----+-----+-----+-----+
```

4 4/6

4.164)

```
+-----------------------------------------------+
|                                               |
+-----------------------------------------------+
+-----------------------------------------------+
|                                               |
+-----------------------------------------------+
+-----+-----+-----+-----+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+-----+-----+-----+-----+
+-----+-----+-----+-----+
| 1/8 | 1/8 | 1/8 | 1/8 |
+-----+-----+-----+-----+
```

3 1/2

4.165) 5 6/7

4.166) 2 9/11

4.167) 16 1/2

4.168) 15 1/3

4.169) 9 1/3

4.170) 6 3/5

4.171)

```
+-----------------------+
|                       |
+-----------------------+


---------------------------------------


+-----+
| 1/4 |
+-----+
```

3/4

4.172)

```
+-----------------------------+
|                             |
+-----------------------------+


---------------------------------------


+-----+
| 1/5 |
+-----+
```

4/5

4.173)

```
+-----------------------------+
|                             |
+-----------------------------+
+-----------------------------+
|                             |
+-----------------------------+


---------------------------------------


+-----+
| 1/5 |
+-----+
```

1 4/5

4.174)

```
+-----------------+
|                 |
+-----------------+
+-----------------+
|                 |
+-----------------+


---------------------------------------


+-----+
| 1/3 |
+-----+
```

1 2/3

4.175) no more modeling after this point -- its too tedious to do in text

2/3

4.176) 3/4

4.177) 2/3

4.178) 2/5

4.179) 2 2/3

4.180) 1 5/7

4.181) 26/9 

4.182) 12/7

4.183) 6 + 7/12

4.184) 12 3/10

4.185) 5 1/5

4.186) 1 11/12

4.187) -41/8

4.188) -757/63

__EXERCISE__

4.6.436) 4 2/5 (too tedious to draw model in text)

4.6.437) 3 2/3 (too tedious to draw model in text)

4.6.438) 3 2/8 (too tedious to draw model in text)

4.6.439) 3 4/6 (too tedious to draw model in text)

4.6.440) 11 2/3

4.6.441) 7 5/9

4.6.442) 14

4.6.443) 11

4.6.444) 10 3/5

4.6.445) 11

4.6.446) 15 1/5

4.6.447) 11 1/3

4.6.448) 1/3 (too tedious to draw model in text)

4.6.449) 1/2 (too tedious to draw model in text)

4.6.450) 1 4/8

4.6.451) 1 2/12

4.6.452) 4 8/20

4.6.453) 6 6/15

4.6.454) 3 6/7

4.6.455) 1 7/9

4.6.456) 6/8

4.6.457) 10/12

4.6.458)

* 9 7/12

4.6.459)

* 7 11/12

4.6.460)

* 6 1/8

4.6.461)

* 16 1/6

4.6.462)

* -7 11/6

4.6.463)

* 5 9/20

4.6.464)

* -1 1/6

4.6.465)

* -2 8/16
* -2 1/2

4.6.466)

* 21/8 * 7/4
* 147/32
* 4 19/32

4.6.467)

* 5/3 * 25/6
* 125/18
* 6 17/18

4.6.468) 6/7

4.6.469) 7/9

4.6.470)

* 17/12 * 12/1
* 17

4.6.471)

* 23/10 * 10/1
* 23

4.6.472)

* 4 -2/12
* 3 10/12
* 3 5/6

4.6.473)

* 8 -2/8
* 7 6/8
* 7 3/4

4.6.474)

* 1/9

4.6.475)

* 4/15

4.6.476)

* 3 1/4

4.6.477)

* 5 3/5

4.6.478)

* 9/20 * 4/3
* 36/60
* 18/30
* 9/15

4.6.479)

* 7/24 * 3/14
* 21/336
* 1/16

4.6.480)

* 17 5/11

4.6.481)

* 13 1/13

4.6.482)

* 9 3/20

4.6.483)

* 7 1/30

4.6.484)

* 80/285
* 16/57

4.6.485)

* 40/108
* 10/27

4.6.486)

* 4 13/24

4.6.487)

* 4 7/45

4.6.488)

* 1 -26/45
* 19/45

4.6.489)

* 1 -8/24
* 16/24
* 2/3

4.6.490) 3 4/8, 3 1/2

4.6.491) 1 -5/12

4.6.492) 5 1/2

4.6.493) 13 1/4

4.6.494)

```
    +-----------------------------------------------+  |  +-----------------------------------------------+ 
  1 |                                               |  |  |                                               | 1
    +-----------------------------------------------+  |  +-----------------------------------------------+ 
    +-----+-----+-----+-----+-----+                    |  +-----------------------------------------------+
5/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |                    |  |                                               | 1
    +-----+-----+-----+-----+-----+                    |  +-----------------------------------------------+ 
                                                       |  +-----+-----+-----+-----+-----+-----+-----+
                                                       |  | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 |       7/8
                                                       |  +-----+-----+-----+-----+-----+-----+-----+
    
                         |                                                          |
                         |                                                          |
                         +-----------------------------+----------------------------+
                                                       |
                                                       v
                                +-----------------------------------------------+
                                |                                               | 1
                                +-----------------------------------------------+
                                +-----------------------------------------------+
                                |                                               | 1
                                +-----------------------------------------------+
                                +-----------------------------------------------+
                                |                                               | 1
                                +-----------------------------------------------+
                                +-----------------------------------------------+
                                |                                               | 1
                                +-----------------------------------------------+
                                +-----+-----+-----+-----+-----+-----+-----+-----+
                                | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1/8 | 1
                                +-----+-----+-----+-----+-----+-----+-----+-----+
                                +-----+-----+-----+-----+
                                | 1/8 | 1/8 | 1/8 | 1/8 |                         4/8
                                +-----+-----+-----+-----+
```

4.6.495)

* a) 4 quarters, 4 1dollar bills, 1 5dollar bill
* b) it'll tell him the number of quarters he'll have remaining in his pocket? this question is too ambiguous

4.6.496) mixed numbers are easier for a person to think about because the numbers they're dealing with are smaller, but i prefer leaving them as fractions, but i prefer leaving them as fractions because I don't have to think about it as whole + fraction, just fraction

4.6.497) mixed numbers are easier for a person to think about because the numbers they're dealing with are smaller, but i prefer leaving them as fractions because I don't have to think about it as whole + fraction, just fraction

## Chapter 4 Section 7

__TRY IT__

4.189)

* a) 3/3 - 2/3 = 1/3  NO
* b) 5/6 - 4/6 = 1/6  YES
* c) -5/6 - 4/6 = -9/6 = -3/2  NO

4.190)

* a) 4/4 - 1/4 = 3/4  NO
* b) -5/8 - 2/8 = -7/8  NO
* c) 5/8 - 2/8 = 3/8  YES

4.191) y = 5/16 - 9/16 = -4/16

4.192) y = 4/15 - 8/15 = -4/15

4.193) a = -8/5 + 3/5 = -5/5

4.194) n = -9/7 + 3/7 = -6/7

4.195) u = -76/12

4.196) m = 92/8

4.197) f = -125

4.198) h = -243

4.199) c = 245

4.200) x = 131

4.201) y = -48

4.202) c = 23

4.203)

* 2n = 70
* n = 70/2
* n = 35

4.204)

* 5y = 90
* y = 45

4.205)

* -4a = 364
* a = -91

4.206)

* -7w = 84
* w = 84/-7
* w = -12

4.207)

* n/7 = -21
* n = -147

4.208)

* n/8 = -56
* n = -448

4.209)

* q/-8 = 72
* q = -576

4.210)

* p/-9 = 81
* p = -729

4.211)

* 2/5f = 16
* f = 16 / 2/5
* f = 16/1 / 2/5
* f = 16/1 * 5/2
* f = 80/2
* f = 40

4.212)

* 3/4f = 21
* f = 21 / 3/4
* f = 21/1 / 3/4
* f = 21/1 * 4/3
* f = 84/3
* f = 28

4.213)

* n / 2/3 = 5/12
* n = 5/12 * 2/3
* n = 10/36
* n = 5/18

4.214)

* c / 3/8 = 4/9
* c = 4/9 * 3/8
* c = 12/72
* c = 4/24
* c = 1/6

4.215)

* 5/8 + x = 1/4
* x = 1/4 - 5/8
* x = 2/8 - 5/8
* x = -3/8

4.216)

* 1 3/4 - x = 4/6
* -x = 4/6 - 1 3/4
* -x = 4/6 - 7/4
* -x = 8/12 - 21/12
* -x = -13/12
* x = 13/12

__EXERCISE__

4.7.498)

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