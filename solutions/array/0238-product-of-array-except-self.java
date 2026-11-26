class Solution {
    public int[] productExceptSelf(int[] nums) {
        int[] ans=new int[nums.length];
        int product=1;
        for(int i=0;i<nums.length;i++) {
            ans[i]=product; // 先写左侧乘积，再纳入当前元素
            product*=nums[i];
        }
        product=1;
        for(int i=nums.length-1;i>=0;i--) {
            ans[i]*=product;
            product*=nums[i]; // 留给左边位置使用的右侧乘积
        }
        return ans;
    }
}
