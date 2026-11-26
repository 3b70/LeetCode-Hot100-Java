import java.util.*;
class Solution {
    public List<Integer> findAnagrams(String s,String p) {
        List<Integer> ans=new ArrayList<>();
        int[] target=new int[26],window=new int[26];
        for(char c:p.toCharArray()) target[c-'a']++;
        int m=p.length();
        for(int r=0;r<s.length();r++) {
            window[s.charAt(r)-'a']++;
            if(r>=m) window[s.charAt(r-m)-'a']--; // 保持固定长度
            if(r>=m-1 && Arrays.equals(window,target)) ans.add(r-m+1);
        }
        return ans;
    }
}
