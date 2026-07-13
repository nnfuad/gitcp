class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        res = []
        for length in range(2, 10):
            max_start = 9 - (length - 1)
            for start in range(1, max_start + 1):
                num = 0
                for i in range(length):
                    num = num * 10 + (start + i)
                if low <= num <= high:
                    res.append(num)
        res.sort()
        return res