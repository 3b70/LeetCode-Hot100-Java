class Solution {
    public int rob(int[] nums) {
        int prev2=0,prev1=0;
        for(int money:nums) {
            int next=Math.max(prev1,prev2+money); // 不偷当前房，或偷当前并跳过前房
            prev2=prev1; prev1=next;
        }
        return prev1;
    }
}
