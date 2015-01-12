Title: Two sum
Date: 2015-01-01 10:00

### problem

>Given an array of integers, find two numbers such that they add up to a specific target number.
>
>The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.
>
>You may assume that each input would have exactly one solution.
>
>Input: numbers={2, 7, 11, 15}, target=9
>
>Output: index1=1, index2=2

### source code
    :::java
    import java.util.HashMap;
    import java.util.Map;

    public class Solution {
        public int[] twoSum(int[] numbers, int target) {
            Map<Integer, Integer> map = new HashMap<Integer, Integer>();
            for (int i = 0; i < numbers.length; i++) {
                map.put(numbers[i], i);
            }

            int tmp;
            int begin = 0;
            int end = 0;
            for (int i = 0; i < numbers.length; i++) {
                tmp = target - numbers[i];
                if (map.containsKey(tmp) && map.get(tmp) != i) {
                    begin = i;
                    end = map.get(tmp);
                    break;
                }
            }
            return new int[]{begin + 1, end + 1};
        }
    }