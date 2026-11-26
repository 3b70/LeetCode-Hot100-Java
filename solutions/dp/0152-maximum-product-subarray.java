class Solution {
    public int maxProduct(int[] nums) {
        int max=nums[0],min=nums[0],best=max;
        for(int i=1;i<nums.length;i++) {
            int x=nums[i],a=max*x,b=min*x; // 先保存两个旧状态的乘积
            max=Math.max(x,Math.max(a,b)); min=Math.min(x,Math.min(a,b));
            best=Math.max(best,max);
        }
        return best;
    }
}
