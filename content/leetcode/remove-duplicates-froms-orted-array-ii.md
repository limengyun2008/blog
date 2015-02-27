Title: Remove Duplicates from Sorted Array II
Date: 2015-01-21 10:00

### problem

从一个有序数组中剔除重复元素，元素允许重复两遍

>Follow up for "Remove Duplicates":
>
>What if duplicates are allowed at most twice?
>
>For example,
>
>Given sorted array A = [1,1,1,2,2,3],
>
>
>Your function should return length = 5, and A is now [1,1,2,2,3].


### solution
取到没取到的元素就index++...

### source code
    :::java
    public class Solution {
        public int removeDuplicates(int[] A) {
            if (A.length == 0) {
                return 0;
            }
            int index = 1;
            int occurence = 1;

            for (int i = 1; i < A.length; i++) {
                if (A[i] != A[index-1]) {
                    A[index++] = A[i];
                    occurence = 1;
                } else {
                    if (occurence < 2) {
                        A[index++] = A[i];
                        occurence++;
                    }
                }
            }
            return index;
        }
    }