class Solution {
    public int[] searchRange(int[] nums,int target) {
        int first=bound(nums,target,false);
        if(first==nums.length || nums[first]!=target) return new int[]{-1,-1};
        return new int[]{first,bound(nums,target,true)-1};
    }
    private int bound(int[] a,int target,boolean upper) {
        int l=0,r=a.length;
        while(l<r) {
            int m=l+(r-l)/2;
            // upper为true时，相等元素也要排除到左边
            if(a[m]<target || (upper && a[m]==target)) l=m+1; else r=m;
        }
        return l;
    }
}
