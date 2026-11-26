import java.util.*;
class Solution {
    public int findKthLargest(int[] nums,int k) {
        PriorityQueue<Integer> heap=new PriorityQueue<>();
        for(int x:nums) {
            heap.offer(x);
            if(heap.size()>k) heap.poll(); // 丢弃较小数，只留下最大的k个
        }
        return heap.peek();
    }
}
