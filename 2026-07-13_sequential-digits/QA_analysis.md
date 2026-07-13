# Sequential Digits

**Difficulty:** Medium

**Link:** https://leetcode.com/problems/sequential-digits/

---

The problem requires finding all integers within a given range [low, high] that have sequential digits. Sequential digits mean each digit is exactly one more than the previous digit (e.g., 123, 234). The solution must return these numbers in sorted order.

### Key Observations:
1. **Sequential Digit Numbers**: These numbers are formed by starting at a digit and incrementing each subsequent digit by 1. For example, starting at 1 with length 3 gives 123.
2. **Generation Strategy**: Generate all possible sequential numbers by varying the starting digit and length. For a given length `L`, the starting digit can range from 1 to `9 - (L - 1)` to ensure the last digit doesn't exceed 9.
3. **Efficiency**: There are only 36 possible sequential numbers (sum of 1+2+...+8 for lengths 2 through 9). This allows generating all candidates upfront, filtering them by the range, and sorting the result.

### Approach:
1. **Generate All Candidates**: Iterate over lengths from 2 to 9. For each length, compute valid starting digits and construct the sequential number.
2. **Filter by Range**: Check if each generated number lies within [low, high].
3. **Sort and Return**: Sort the filtered numbers and return them.

### Time and Space Complexity:
- **Time**: O(1) since the number of candidates is fixed (36 numbers).
- **Space**: O(1) as the maximum list size is 36 elements.

This approach is optimal due to the small and fixed number of candidates.