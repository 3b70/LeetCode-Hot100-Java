import java.util.*;
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] dp=new int[nums.length]; Arrays.fill(dp,1); int best=0;
        for(int i=0;i<nums.length;i++) {
            for(int j=0;j<i;j++) if(nums[j]<nums[i]) dp[i]=Math.max(dp[i],dp[j]+1);
            best=Math.max(best,dp[i]); // 任意位置都可作为最优序列的结尾
        }
        return best;
    }
}
