class Solution {
    public void moveZeroes(int[] nums) {
        int write = 0;
        for (int x : nums) {
            if (x != 0) nums[write++] = x; // 稳定地压紧非零元素
        }
        while (write < nums.length) nums[write++] = 0; // 剩余位置补零
    }
}
