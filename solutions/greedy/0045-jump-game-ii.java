class Solution {
    public int jump(int[] nums) {
        int end=0,far=0,steps=0;
        for(int i=0;i<nums.length-1;i++) {
            far=Math.max(far,i+nums[i]);
            if(i==end) { steps++; end=far; } // 当前层结束，进入下一跳覆盖区间
        }
        return steps;
    }
}
