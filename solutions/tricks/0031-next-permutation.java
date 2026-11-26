class Solution {
    public void nextPermutation(int[] nums) {
        int i=nums.length-2;
        while(i>=0 && nums[i]>=nums[i+1]) i--;
        if(i>=0) {
            int j=nums.length-1;
            while(nums[j]<=nums[i]) j--;
            swap(nums,i,j); // 右侧第一个更大值带来最小增幅
        }
        for(int l=i+1,r=nums.length-1;l<r;l++,r--) swap(nums,l,r); // 后缀恢复最小顺序
    }
    private void swap(int[] a,int i,int j) { int t=a[i]; a[i]=a[j]; a[j]=t; }
}
