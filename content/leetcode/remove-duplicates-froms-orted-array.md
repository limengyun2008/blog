Title: Remove Duplicates from Sorted Array 
Date: 2015-01-20 10:00

### problem

从一个有序数组中剔除重复元素

>Given a sorted array, remove the duplicates in place such that each element appear only once and return the new length.
>
>Do not allocate extra space for another array, you must do this in place with constant memory.
>
>For example,
>
>Given input array A = [1,1,2],
>
>
>Your function should return length = 2, and A is now [1,2].


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

            for (int i = 1; i < A.length; i++) {
                if (A[i] != A[index-1]) {
                    A[index++] = A[i];
                }
            }
            return index;
        }
    }