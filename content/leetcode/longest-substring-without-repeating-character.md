Title: Longest Substring Without Repeating Characters
Date: 2015-01-03 10:00

### problem

>Given a string, find the length of the longest substring without repeating characters. For example, the longest substring without repeating letters for "abcabcbb" is "abc", which the length is 3. For "bbbbb" the longest substring is "b", with the length of 1.

### solution
从前往后找，碰到重复元素更新字符串，要注意这个判定条件<b>map.get(s.charAt(end)) >= begin</b>

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
