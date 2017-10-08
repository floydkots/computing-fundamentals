# 2048 (Merge)

## See it in action
Find the implementation at [codeskulptor.org](http://www.codeskulptor.org/#user43_ItQ95QAuVw_2.py)

## Mini-project description
For this assignment, you will implement a function `merge(line)` that models the process of merging all of the tile values in a single row or column. This function takes the list `line` as a parameter and returns a new list with the tile values from `line` slid towards the front of the list and merged. Note that you should return a new list and you should not modify the input list. This is one of the more challenging parts of implementing the game.

In this function, you are always sliding the values in the list towards the front of the list (the list position with index 0). You will make sure you order the entries in `line` appropriately when you call this function later in the next assignment. Empty grid squares with no displayed value will be assigned a value of zero in our representation.

For example, if a row of the board started as follows:

![Row of the board started as follow](https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/sSTmceJOEeWIdgqHxZs34w_85e344ce5c725da880fe30d8ad1c51e2_poc_2022.png?expiry=1507593600000&hmac=1AszoUx0qaliB6hSuX-mWVnbszsS7vPJeXvbT7WCVCM)

And you slide the tiles left, the row would become:

![After sliding tiles left](https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/1gAFE-JOEeWIdgqHxZs34w_e4876fafcc7de8f4fddac6a744621d76_poc_4200.png?expiry=1507593600000&hmac=F1RVWS50LqmCP6KfuSQ0QeuoN2ipZrDW1u_nKNClyII)

Note that the two leftmost tiles merged to become a 4 and the third 2 just slides over next to the 4.

A given tile can only merge once on any given turn, although many pairs of tiles could merge on a single turn.

For the above example, the input to the `merge` function would be the list `[2, 0, 2, 2]`. The function should then produce the output `[4, 2, 0, 0]`. We suggest you begin to implement this function as follows:

1. Start with a result list that contains the same number of 0's as the length of the `line` argument.
2. Iterate over the `line` input looking for non-zero entries. For each non-zero entry, put the value into the next available entry of the result list (starting at position 0).

Notice if you only follow this process, you would end up with the result `[2, 2, 2, 0]`.

Now you should think through what you should add to your function in order to merge tiles. Keep in mind, however, that any tile should only be merged once and that these merges should happen in order from lowest index to highest index. For instance, on the input `[2, 0, 2, 4]`, the result should be `[4, 4, 0, 0]`, **not** `[8, 0, 0, 0]`.

Note that there are many ways to implement the merge function. The objective of this project is for you to use what you've learned in our previous classes to implement a complex function. You have already learned all of the Python required to implement `merge`, so the challenge is to think carefully about what the function does and how to best accomplish that.

Here is one basic strategy to implement the merge function:

1. Iterate over the input and create an output list that has all of the non-zero tiles slid over to the beginning of the list with the appropriate number of zeroes at the end of the list.
2. Iterate over the list created in the previous step and create another new list in which pairs of tiles in the first list are replaced with a tile of twice the value and a zero tile.
3. Repeat step one using the list created in step two to slide the tiles to the beginning of the list again.

This is not the most efficient way of implementing `merge`. While it is fine to implement it in this way, we challenge you to think of other ways of doing it that do not require creating so many lists. Ultimately, how you approach the problem is up to you.

As you work on your `merge` function, here are some simple tests you should try:

- `[2, 0, 2, 4]` should return `[4, 4, 0, 0]`
- `[0, 0, 2, 2]` should return `[4, 0, 0, 0]`
- `[2, 2, 0, 0]` should return `[4, 0, 0, 0]`
- `[2, 2, 2, 2, 2]` should return `[4, 4, 2, 0, 0]`
- `[8, 16, 16, 8]` should return `[8, 32, 8, 0]`

These tests are by no means exhaustive and are just meant to get you started.
