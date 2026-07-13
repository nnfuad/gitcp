class Solution:
    def sequentialDigits(self, low: int, high: int) -> list[int]:
        result = []
        for length in range(len(str(low)), len(str(high)) + 1):
            for start in range(1, 11 - length):
                num = 0
                for i in range(length):
                    num = num * 10 + start + i
                if low <= num <= high:
                    result.append(num)
        return result