import java.util.*;
class Solution {
    private static final String[] LETTERS={"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
    public List<String> letterCombinations(String digits) {
        List<String> ans=new ArrayList<>();
        if(!digits.isEmpty()) dfs(digits,0,new StringBuilder(),ans);
        return ans;
    }
    private void dfs(String s,int index,StringBuilder path,List<String> ans) {
        if(index==s.length()) { ans.add(path.toString()); return; }
        for(char c:LETTERS[s.charAt(index)-'0'].toCharArray()) {
            path.append(c); dfs(s,index+1,path,ans);
            path.deleteCharAt(path.length()-1); // 删除本层选择，保留前缀
        }
    }
}
