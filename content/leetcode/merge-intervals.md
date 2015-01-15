Title: Merge Intervals 
Date: 2015-01-05 10:00

### problem

>Given a collection of intervals, merge all overlapping intervals.
>
> <br/>
>For example,
>
>Given <b>[1,3],[2,6],[8,10],[15,18],</b>
>
>return <b>[1,6],[8,10],[15,18].</b>

### solution
见注释

### source code
    :::java
    /**
     * Definition for an interval.
     * public class Interval {
     *     int start;
     *     int end;
     *     Interval() { start = 0; end = 0; }
     *     Interval(int s, int e) { start = s; end = e; }
     * }
     */
    public class Solution {
        public List<Interval> merge(List<Interval> intervals) {
            // 把区间按照start排序
            Collections.sort(intervals, new Comparator<Interval>() {
                @Override
                public int compare(Interval interval1, Interval interval2) {
                    return interval1.start - interval2.start;
                }
            });

            List<Interval> result = new ArrayList<Interval>();
            Interval tmp = null;
            for (Interval interval : intervals) {
                if (tmp == null) {
                    tmp = interval;
                } else {
                    if (tmp.end < interval.start) {
                        // 如果一个区间跟上一个区间没有相交，那么直接把上一个区间加入结果
                        result.add(tmp);
                        tmp = interval;
                    } else if (tmp.end >= interval.start && tmp.end < interval.end) {
                        // 如果一个区间跟上一个区间有相交的部分，那么就直接把上一个区间的end延长为该区间的end
                        tmp.end = interval.end;
                    }
                    // 剩下的case 就是一个区间被上一个区间包裹住，可以直接丢弃
                }
            }

            if (tmp != null) {
                result.add(tmp);
            }
            return result;
        }
    }
