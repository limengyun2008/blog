Title: Best Time to Buy and Sell Stock II
Date: 2015-01-11 10:00

### problem
无限次买卖股票的最大收益
>Say you have an array for which the ith element is the price of a given stock on day i.

>Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times). However, you may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

### solution

对于无限次交易的情况，只需要逢涨买入，下跌时抛出，则一定是最大收益。

### source code
    :::java
    public class Solution {
        public int maxProfit(int[] prices) {
            if (prices.length == 0) {
                return 0;
            }
            
            int buy = prices[0];
            int profit = 0;
            for (int i = 1 ; i < prices.length ; i++) {
                if (prices[i] > buy) {
                    profit += prices[i] - buy;
                }
                buy = prices[i];
            }
            
            return profit;
        }
    }
