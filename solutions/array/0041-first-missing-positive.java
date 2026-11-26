class Solution {
    public int firstMissingPositive(int[] nums) {
        int n=nums.length;
        for(int i=0;i<n;i++) {
            // 重复值已就位时停止，避免无限交换
            while(nums[i]>=1 && nums[i]<=n && nums[nums[i]-1]!=nums[i]) {
                int target=nums[i]-1;
                int t=nums[target]; nums[target]=nums[i]; nums[i]=t;
            }
        }
        for(int i=0;i<n;i++) if(nums[i]!=i+1) return i+1;
        return n+1;
    }
}
