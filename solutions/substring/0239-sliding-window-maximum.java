import java.util.*;
class Solution {
    public int[] maxSlidingWindow(int[] nums,int k) {
        int[] ans=new int[nums.length-k+1];
        Deque<Integer> q=new ArrayDeque<>();
        for(int i=0;i<nums.length;i++) {
            while(!q.isEmpty() && q.peekFirst()<=i-k) q.removeFirst(); // 去掉过期下标
            while(!q.isEmpty() && nums[q.peekLast()]<=nums[i]) q.removeLast();
            q.addLast(i); // 保留从大到小的候选
            if(i>=k-1) ans[i-k+1]=nums[q.peekFirst()];
        }
        return ans;
    }
}
