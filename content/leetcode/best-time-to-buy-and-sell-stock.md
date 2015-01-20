Title: Best Time to Buy and Sell Stock
Date: 2015-01-10 10:00

### problem

>Say you have an array for which the ith element is the price of a given stock on day i.

>If you were only permitted to complete at most one transaction (ie, buy one and sell one share of the stock), design an algorithm to find the maximum profit.

### solution
这是一个系列题，分别为
仅限[一次交易](/leetcode/best-time-to-buy-and-sell-stock.html)，
[无限次交易](/leetcode/best-time-to-buy-and-sell-stock-ii.html)，
和[仅限两次交易](/leetcode/best-time-to-buy-and-sell-stock-iii.html)三个版本。

对于仅有一次交易的情况，采用动态规划，计算当前最大的收益即可

### source code
    :::java
    public class Solution {
        public int maxProfit(int[] prices) {
            int buy = Integer.MIN_VALUE;
            int sell = 0;

            for (int price : prices) {
                sell = Math.max(sell, buy + price);
                buy = Math.max(buy, -price);
            }
            return sell;
        }
    }
