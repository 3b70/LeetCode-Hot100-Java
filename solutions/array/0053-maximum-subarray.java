class Solution {
    public int maxSubArray(int[] nums) {
        int end=nums[0],best=end;
        for(int i=1;i<nums.length;i++) {
            end=Math.max(nums[i],end+nums[i]); // 延长旧区间或从当前位置重启
            best=Math.max(best,end);
        }
        return best;
    }
}
