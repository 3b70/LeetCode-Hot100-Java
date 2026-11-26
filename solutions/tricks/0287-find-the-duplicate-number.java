class Solution {
    public int findDuplicate(int[] nums) {
        int slow=0,fast=0;
        do { slow=nums[slow]; fast=nums[nums[fast]]; } while(slow!=fast);
        int p=0;
        while(p!=slow) { p=nums[p]; slow=nums[slow]; } // 回起点后同速找环入口
        return p;
    }
}
