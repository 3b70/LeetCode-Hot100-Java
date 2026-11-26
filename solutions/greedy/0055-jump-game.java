class Solution {
    public boolean canJump(int[] nums) {
        int far=0;
        for(int i=0;i<nums.length;i++) {
            if(i>far) return false; // 先检查可达，再读取此位置的跳跃贡献
            far=Math.max(far,i+nums[i]);
            if(far>=nums.length-1) return true;
        }
        return true;
    }
}
