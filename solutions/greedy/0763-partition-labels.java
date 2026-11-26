import java.util.*;
class Solution {
    public List<Integer> partitionLabels(String s) {
        int[] last=new int[26];
        for(int i=0;i<s.length();i++) last[s.charAt(i)-'a']=i;
        List<Integer> ans=new ArrayList<>(); int start=0,end=0;
        for(int i=0;i<s.length();i++) {
            end=Math.max(end,last[s.charAt(i)-'a']); // 当前段必须覆盖所有已遇字符的最后位置
            if(i==end) { ans.add(i-start+1); start=i+1; }
        }
        return ans;
    }
}
