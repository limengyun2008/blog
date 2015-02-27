Title: Best Time to Buy and Sell Stock III
Date: 2015-01-12 10:00

### problem
仅限2次买卖股票的最大收益
>Say you have an array for which the ith element is the price of a given stock on day i.

>Design an algorithm to find the maximum profit. You may complete at most two transactions.

>Note:
>You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

### solution

跟[一次交易](/leetcode/best-time-to-buy-and-sell-stock.html)的版本类似，但是动态规划的过程要繁琐一点，这道题我自己思路错了，去查了discuss，贴出一个个人认为最好的解法。

大体思路就是保证不论第一次还是第二次，也不论买入时和卖出时，都保证当前的净收益是最大的，则最后的收益也是最大的。这种解法可以很方便的扩展到N次交易的情况。

### source code
    :::java
    public class Solution {
        public int maxProfit(int[] prices) {
            int buy1 = Integer.MIN_VALUE;
            int sell1 = 0;
            int buy2 = Integer.MIN_VALUE;
            int sell2 = 0;
            for (int price : prices) {
                sell2 = Math.max(sell2, price + buy2);
                buy2 = Math.max(buy2, sell1 - price);
                sell1 = Math.max(sell1, price + buy1);
                buy1 = Math.max(buy1, -price);
            }
            return sell2;
        }
    }
