import java.util.*;
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> ans=new ArrayList<>(); dfs(n,0,0,new StringBuilder(),ans); return ans;
    }
    private void dfs(int n,int left,int right,StringBuilder path,List<String> ans) {
        if(path.length()==2*n) { ans.add(path.toString()); return; }
        if(left<n) {
            path.append('('); dfs(n,left+1,right,path,ans); path.deleteCharAt(path.length()-1);
        }
        if(right<left) { // 只允许用已有的左括号来匹配
            path.append(')'); dfs(n,left,right+1,path,ans); path.deleteCharAt(path.length()-1);
        }
    }
}
