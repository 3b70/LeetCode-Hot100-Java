import java.util.*;
class Solution {
    public List<List<String>> partition(String s) {
        int n=s.length(); boolean[][] pal=new boolean[n][n];
        for(int i=n-1;i>=0;i--) for(int j=i;j<n;j++) {
            pal[i][j]=s.charAt(i)==s.charAt(j) && (j-i<2 || pal[i+1][j-1]);
        }
        List<List<String>> ans=new ArrayList<>(); dfs(s,0,pal,new ArrayList<>(),ans); return ans;
    }
    private void dfs(String s,int start,boolean[][] pal,List<String> path,List<List<String>> ans) {
        if(start==s.length()) { ans.add(new ArrayList<>(path)); return; }
        for(int end=start;end<s.length();end++) if(pal[start][end]) {
            path.add(s.substring(start,end+1)); dfs(s,end+1,pal,path,ans);
            path.remove(path.size()-1); // 撤销本次切片
        }
    }
}
