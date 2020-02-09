package com.offbynull.wholenum;

import java.util.Arrays;
import static java.util.Arrays.stream;
import static java.util.stream.Collectors.joining;
import java.util.stream.IntStream;
import static java.util.stream.IntStream.concat;
import static java.util.stream.IntStream.range;
import org.apache.commons.lang3.ArrayUtils;

public class Number {
    private int[] digits;
    
    public static Number createAllZeros(int length) {
        return new Number(range(0, length).map(i -> 0).toArray());
    }
    
    public static Number createFromDigits(int... digits) {
        return new Number(digits);
    }
    
    private Number(int[] digits) {
        this.digits = Arrays.copyOf(digits, digits.length);
    }
    
    public void prependZerosIfShorterThan(int maxLen) {
        this.digits = concat(
                range(digits.length, maxLen).map(i -> 0),
                stream(digits)
        ).toArray();
    }
    
    public void appendZerosIfShorterThan(int maxLen) {
        this.digits = concat(
                stream(digits),
                range(digits.length, maxLen).map(i -> 0)
        ).toArray();
    }
    
    public void appendZeros(int len) {
        this.digits = concat(
                stream(digits),
                range(0, len).map(i -> 0)
        ).toArray();
    }
    
    public void prepend(Number other) {
        this.digits = concat(stream(other.digits), stream(this.digits)).toArray();
    }

    public void prependDigits(int... digits) {
        this.digits = concat(IntStream.of(digits), stream(this.digits)).toArray();
    }
    
    public int getDigit(int i) {
        i = digits.length - i - 1;
        return digits[i];
    }
    
    public void setDigit(int i, int digit) {
        i = digits.length - i - 1;
        digits[i] = digit;
    }
    
    public int length() {
        return digits.length;
    }
    
    public Number copy() {
        return new Number(digits);
    }
    
    @Override
    public String toString() {
        return stream(digits).mapToObj(d -> d + "").collect(joining());
    }
    
    
    
    
    
    public static String isolateLast(Number n) {
        return isolate(n, n.length() - 1);
    }
    
    public static String isolate(Number n, int... idxes) {
        String ret = "";
        for (int i = n.length() - 1; i >= 0; i--) {
            int finalI = i;
            ret += IntStream.of(idxes).anyMatch(idx -> finalI == idx) ? " [" + n.getDigit(i) + "] " : " " + n.getDigit(i) + " ";
        }
        return ret;
    }
}
