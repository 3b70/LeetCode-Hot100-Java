import java.util.*;
class Solution {
    public int largestRectangleArea(int[] heights) {
        Deque<Integer> stack=new ArrayDeque<>(); int best=0,n=heights.length;
        for(int i=0;i<=n;i++) {
            int h=i==n?0:heights[i]; // 末尾虚拟0触发所有正高度结算
            while(!stack.isEmpty() && heights[stack.peek()]>h) {
                int height=heights[stack.pop()];
                int left=stack.isEmpty()?-1:stack.peek();
                best=Math.max(best,height*(i-left-1));
            }
            if(i<n) stack.push(i); // 不把虚拟下标压栈
        }
        return best;
    }
}
