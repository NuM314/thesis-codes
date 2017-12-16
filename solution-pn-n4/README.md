# Algorithm for calculating terms of [A049311](https://oeis.org/A049311)
`a(n)` is the number of (0,1) matrices with `n` ones up to row and column permutations.

For a given `n` the code calculates `a(1), a(2), ..., a(n)`.

### Usage:
```
python calculate.py
```

### Example:
```
Enter n: 15
a(1) = 1
a(2) = 3
a(3) = 6
a(4) = 16
a(5) = 34
a(6) = 90
a(7) = 211
a(8) = 558
a(9) = 1430
a(10) = 3908
a(11) = 10725
a(12) = 30825
a(13) = 90156
a(14) = 273234
a(15) = 848355
```

Algorithm complexity is O(p(n) n^4).

Calculation of a(15) takes about 2 seconds.

Calculation of a(30) takes about 15 minutes.
