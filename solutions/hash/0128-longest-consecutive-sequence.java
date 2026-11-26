import java.util.*;
class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) set.add(x);
        int best = 0;
        for (int x : set) {
            // 只从没有前驱的数字开始，避免重复扫描整条序列
            if (x != Integer.MIN_VALUE && set.contains(x - 1)) continue;
            int y = x, length = 1;
            while (y != Integer.MAX_VALUE && set.contains(y + 1)) { y++; length++; }
            best = Math.max(best, length);
        }
        return best;
    }
}
