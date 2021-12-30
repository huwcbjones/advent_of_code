1) Simplify code to
```py
w = int(input())
x = int((z % 26) + a != w)
z //= c
z *= 25 * x + 1
z += (w + b) * x
```

2) Create table of table to digits

| Digit | A   | B   | C   |
|-------|-----|-----|-----|
| 0     | 12  | 12  | 1   |
| 1     | 12  | 7   | 1   |
| 2     | 10  | 8   | 1   |
| 3     | 12  | 8   | 1   |
| 4     | 11  | 15  | 1   |
| 5     | -16 | 12  | 26  |
| 6     | 10  | 8   | 1   |
| 7     | -11 | 13  | 26  |
| 8     | -13 | 3   | 26  |
| 9     | 13  | 13  | 1   |
| 10    | -8  | 3   | 26  |
| 11    | -1  | 9   | 26  |
| 12    | -4  | 4   | 26  |
| 13    | -14 | 13  | 26  |

3) Decode simplified program:
   1) Program behaves like a stack
   2) If C == 1, you're effectively pushing w+a
   3) If C == 26, you're effectively popping w-b
4) This means that you can derive the rules:
<pre>
I[0] + 12 - 14 = I[13]
I[1] +  7 -  4 = I[12]
I[2] +  8 -  1 = I[11]
I[3] +  8 - 13 = I[8]
I[4] + 15 - 16 = I[5]
I[6] +  8 - 11 = I[7]
I[9] + 13 -  8 = I[10]
</pre>
Simplified...
<pre>I[0] - 2 = I[13]
I[1] + 3 = I[12]
I[2] + 7 = I[11]
I[3] - 5 = I[8]
I[4] - 1 = I[5]
I[6] - 3 = I[7]
I[9] + 5 = I[10]
</pre>
5) Part 1: Determine max number
<pre>
                   |1|1|1|1|
0|1|2|3|4|5|6|7|8|9|0|1|2|3|
9|6|2|9|9|8|9|6|4|4|9|9|9|7|
</pre>
6) Part 2: Determine min number
<pre>
                   |1|1|1|1|
0|1|2|3|4|5|6|7|8|9|0|1|2|3|
3|1|1|6|2|1|4|1|1|1|6|8|4|1|
</pre>
