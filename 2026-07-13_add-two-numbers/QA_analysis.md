# Add Two Numbers

**Difficulty:** Medium

**Link:** https://leetcode.com/problems/add-two-numbers/

---

The problem requires adding two numbers represented as linked lists in reverse order. Each node contains a single digit. The solution must handle varying lengths of input lists and carry propagation during addition.

### Optimal Approach
- **Traversal with Carry Handling**: Traverse both lists simultaneously, adding corresponding digits along with any carry from the previous step. This ensures we process each digit exactly once.
- **Dummy Head for Result List**: Using a dummy head simplifies the creation of the result linked list, avoiding edge cases for the initial node.
- **Edge Cases Handled**: Properly manages when one list is longer than the other and when a final carry remains after processing all digits.

### Time and Space Complexity
- **Time Complexity**: O(max(N, M)), where N and M are the lengths of the two input lists. We traverse each list once.
- **Space Complexity**: O(max(N, M)) for the result linked list, which can be one node longer than the longer input due to carry.

### Solution Code
The implementation uses a dummy node to build the result list iteratively, processing each digit and carry until all inputs and the carry are exhausted.