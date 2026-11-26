import java.util.HashMap;
import java.util.Map;
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            // 先查左侧元素，避免使用当前下标两次
            if (seen.containsKey(need)) return new int[]{seen.get(need), i};
            seen.put(nums[i], i); // 数值映射到已扫描的下标
        }
        return new int[0];
    }
}
