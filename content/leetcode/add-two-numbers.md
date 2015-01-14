Title: Add Two Numbers
Date: 2015-01-02 10:00

### problem

>You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
>
>Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
>
>Output: 7 -> 0 -> 8

### solution
高精度加法，考细致程度，提交了好几次才Accept……

### source code
    :::java
    public class Solution {
        public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
            ListNode head = null;
            ListNode end = null;
            int up = 0;
            while (l1 != null || l2 != null) {
                int val;
                if (l1 == null) {
                    val = l2.val;
                } else if (l2 == null) {
                    val = l1.val;
                } else {
                    val = l1.val + l2.val;
                }
                val += up;
                up = val / 10;
                val = val % 10;
                
                if (head == null) {
                    head = new ListNode(val);
                    end = head;
                } else {
                    end.next = new ListNode(val);
                    end = end.next;
                }
                if (l1 != null) {
                    l1 = l1.next;
                }
                if (l2 != null) {
                    l2 = l2.next;
                }
            }
            if (up > 0) {
                end.next = new ListNode(up);
            }

            return head;
        }
    }