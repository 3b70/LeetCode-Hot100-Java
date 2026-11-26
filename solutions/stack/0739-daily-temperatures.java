import java.util.*;
class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int[] ans=new int[temperatures.length]; Deque<Integer> stack=new ArrayDeque<>();
        for(int i=0;i<temperatures.length;i++) {
            while(!stack.isEmpty() && temperatures[i]>temperatures[stack.peek()]) {
                int p=stack.pop(); ans[p]=i-p; // 当前日是旧日期遇到的第一个更暖日
            }
            stack.push(i);
        }
        return ans;
    }
}
