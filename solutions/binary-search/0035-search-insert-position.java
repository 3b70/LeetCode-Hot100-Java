class Solution {
    public int searchInsert(int[] nums,int target) {
        int l=0,r=nums.length;
        while(l<r) {
            int m=l+(r-l)/2;
            if(nums[m]<target) l=m+1; else r=m; // 保留第一个不小于target的位置
        }
        return l;
    }
}
