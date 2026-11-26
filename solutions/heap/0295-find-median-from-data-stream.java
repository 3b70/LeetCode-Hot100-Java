import java.util.*;
class MedianFinder {
    private final PriorityQueue<Integer> low=new PriorityQueue<>(Comparator.reverseOrder());
    private final PriorityQueue<Integer> high=new PriorityQueue<>();
    public MedianFinder() {}
    public void addNum(int num) {
        low.offer(num); high.offer(low.poll()); // 把左半最大值交给右半
        if(high.size()>low.size()) low.offer(high.poll()); // 恢复大小不变量
    }
    public double findMedian() {
        if(low.size()>high.size()) return low.peek();
        return ((double)low.peek()+high.peek())/2;
    }
}
