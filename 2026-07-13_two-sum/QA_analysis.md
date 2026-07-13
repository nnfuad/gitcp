# Two Sum

**Difficulty:** Easy

**Link:** https://leetcode.com/problems/two-sum/

---

## Problem Analysis

### Understanding the Problem
We need to find two distinct indices in an array where the corresponding values sum to a given target. Key constraints:
- Exactly one solution exists
- Cannot use the same element twice
- Return indices in any order

### Approaches

**1. Brute Force - O(n²) Time, O(1) Space**
- For each element, check all other elements
- Simple but inefficient for large inputs

**2. Hash Map - O(n) Time, O(n) Space** (Optimal)
- Use a dictionary to store value → index mapping
- For each element, check if (target - current_value) exists in the map
- Single pass through the array

### Why Hash Map is Optimal
- Time: O(n) - single traversal
- Space: O(n) - storing at most n elements
- Meets the follow-up requirement of < O(n²)

### Edge Cases Handled
- Negative numbers: Hash map works with any integer values
- Duplicate values: Store index, overwrite if needed (but problem guarantees one solution)
- Same element twice: Check complement before storing current index

### Solution Walkthrough
For nums = [2,7,11,15], target = 9:
1. i=0, num=2, complement=7, not in map → store {2:0}
2. i=1, num=7, complement=2, found at index 0 → return [0,1]

This gives us the answer in a single pass!