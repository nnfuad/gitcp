class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Find indices of two numbers that add up to target.
        Uses hash map for O(n) time complexity.
        
        Args:
            nums: List of integers
            target: Target sum value
            
        Returns:
            List of two indices whose values sum to target
        """
        # Hash map to store value -> index mapping
        num_to_index = {}
        
        for i, num in enumerate(nums):
            # Calculate what value we need to find
            complement = target - num
            
            # If complement exists in our map, we found the solution
            if complement in num_to_index:
                return [num_to_index[complement], i]
            
            # Store current number and its index for future lookups
            num_to_index[num] = i
        
        # Problem guarantees exactly one solution exists
        # This line is unreachable but satisfies type checker
        return []