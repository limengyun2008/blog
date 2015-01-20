Title: Median of Two Sorted Arrays
Date: 2015-01-04 10:00

### problem
两个已排序的数组取中位数
>There are two sorted arrays A and B of size m and n respectively. Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

### solution
一直只取两个数组中最小的，只需要取到 total / 2 + 1 个数就可以了。貌似完全不是标注的Hard级别。

### source code
    :::java
    public class Solution {
        public double findMedianSortedArrays(int A[], int B[]) {
            int total = A.length + B.length;
            int last = 0;
            int current = 0;
            int aIndex = 0;
            int bIndex = 0;
            while (aIndex < A.length || bIndex < B.length) {
                last = current;
                if (aIndex < A.length && bIndex < B.length) {
                    if (A[aIndex] > B[bIndex]) {
                        current = B[bIndex++];
                    } else {
                        current = A[aIndex++];
                    }
                } else if (aIndex < A.length) {
                    current = A[aIndex++];
                } else {
                    current = B[bIndex++];
                }

                if (aIndex + bIndex == total / 2 + 1) {
                    break;
                }
            }

            if (total % 2 == 0) {
                return (current + last) / 2.0;
            } else {
                return current;
            }
        }
    }
