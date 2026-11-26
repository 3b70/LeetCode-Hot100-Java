class Solution {
    public int trap(int[] height) {
        int l=0,r=height.length-1,lm=0,rm=0,water=0;
        while(l<r) {
            lm=Math.max(lm,height[l]); rm=Math.max(rm,height[r]);
            // 较低的已知最高墙足以确定本侧水位
            if(lm<=rm) { water+=lm-height[l]; l++; }
            else { water+=rm-height[r]; r--; }
        }
        return water;
    }
}
