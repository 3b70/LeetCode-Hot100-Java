class Solution {
    public int maxArea(int[] height) {
        int left=0, right=height.length-1, best=0;
        while (left < right) {
            best=Math.max(best,(right-left)*Math.min(height[left],height[right]));
            // 舍弃短板，才可能提高下一次的限制高度
            if (height[left] < height[right]) left++; else right--;
        }
        return best;
    }
}
