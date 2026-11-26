class Solution {
    public void rotate(int[] nums,int k) {
        if(nums.length==0) return;
        k%=nums.length;
        reverse(nums,0,nums.length-1); // 先交换前后两段的整体位置
        reverse(nums,0,k-1);
        reverse(nums,k,nums.length-1); // 恢复各段内部次序
    }
    private void reverse(int[] a,int l,int r) {
        while(l<r) { int t=a[l]; a[l++]=a[r]; a[r--]=t; }
    }
}
