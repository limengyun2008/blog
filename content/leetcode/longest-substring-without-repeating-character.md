Title: Longest Substring Without Repeating Characters
Date: 2015-01-03 10:00

### problem
从一个字符串中寻找最长的没有重复元素的子串
>Given a string, find the length of the longest substring without repeating characters. For example, the longest substring without repeating letters for "abcabcbb" is "abc", which the length is 3. For "bbbbb" the longest substring is "b", with the length of 1.

### solution
从前往后找，碰到重复元素更新字符串（begin向前进），要注意这个判定条件`map.get(s.charAt(end)) >= begin` 否则会把已经移除的元素又重新加进去

### source code
    :::java
    public class Solution {
        public int lengthOfLongestSubstring(String s) {
            Map<Character, Integer> map = new HashMap<Character, Integer>();
            int max = 0;
            int begin = 0;
            int end = 0;
            while (end < s.length()) {
                if (map.containsKey(s.charAt(end)) && map.get(s.charAt(end)) >= begin) {
                    begin = map.get(s.charAt(end)) + 1;
                }
                map.put(s.charAt(end), end);
                end++;
                if ( (end - begin) > max) {
                    max = end - begin;
                }
            }
            return max;
        }
    }
