# Sequential Digits

**Difficulty:** Medium

**Link:** https://leetcode.com/problems/sequential-digits/

---

The problem requires finding all integers within a given range [low, high] that have sequential digits. Sequential digits mean each digit is exactly one more than the previous digit, forming numbers like 123 or 12345.

Optimal Approach:
To generate all possible sequential numbers efficiently, we can iterate over all possible lengths (from 2 to 9 digits) and starting digits (from 1 to 9 - length + 1). For each valid combination, we construct the number by concatenating consecutive digits. This approach ensures that all sequential numbers are generated in sorted order since longer numbers (with more digits) are naturally larger than shorter ones, and within the same length, numbers start from the smallest possible digit first.

Time Complexity: O(1) because there are only 36 possible sequential numbers (sum of 8+7+6+...+1 = 36), making the algorithm constant time regardless of input size.

Space Complexity: O(1) as well, since the maximum number of results is 36 elements.

This approach is optimal because it avoids generating numbers outside the required range and leverages the inherent ordering of sequential numbers.