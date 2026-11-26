class Solution {
    public int singleNumber(int[] nums) {
        int ans=0;
        for(int x:nums) ans^=x; // 相同位模式出现两次后抵消
        return ans;
    }
}
