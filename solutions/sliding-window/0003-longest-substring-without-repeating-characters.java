import java.util.*;
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> window=new HashSet<>();
        int left=0,best=0;
        for(int right=0;right<s.length();right++) {
            char c=s.charAt(right);
            // 不断收缩，直到当前字符可以安全加入
            while(window.contains(c)) window.remove(s.charAt(left++));
            window.add(c);
            best=Math.max(best,right-left+1);
        }
        return best;
    }
}
