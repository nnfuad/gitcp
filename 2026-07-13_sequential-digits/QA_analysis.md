# Sequential Digits

**Difficulty:** Medium

**Link:** https://leetcode.com/problems/sequential-digits/

---

## Problem Analysis
The problem asks us to find all integers in the range [low, high] (inclusive) that have sequential digits. An integer has sequential digits if each digit in the number is one more than the previous digit. The output should be a sorted list of these integers.

## Optimal Approach
To solve this problem, we can use a brute force approach by iterating over all possible lengths of the numbers in the range [low, high]. For each length, we generate all possible sequential numbers and check if they are within the given range. This approach ensures we find all numbers with sequential digits.

## Time and Space Complexity
The time complexity of this approach is O(n), where n is the number of digits in the high number. The space complexity is O(n) as well, as in the worst case, we might need to store all numbers in the range [low, high].

## Solution
The solution involves iterating over all possible lengths of numbers, generating sequential numbers, and checking if they are within the given range.