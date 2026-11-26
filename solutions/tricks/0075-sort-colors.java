class Solution {
    public void sortColors(int[] nums) {
        int zero=0,i=0,two=nums.length-1;
        while(i<=two) {
            if(nums[i]==0) { swap(nums,i,zero); i++; zero++; }
            else if(nums[i]==2) { swap(nums,i,two); two--; } // 换来的元素仍须检查
            else i++;
        }
    }
    private void swap(int[] a,int i,int j) { int t=a[i]; a[i]=a[j]; a[j]=t; }
}
