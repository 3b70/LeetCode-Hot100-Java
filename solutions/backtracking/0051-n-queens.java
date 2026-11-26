import java.util.*;
class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> ans=new ArrayList<>();
        dfs(0,n,new int[n],new boolean[n],new boolean[2*n-1],new boolean[2*n-1],ans); return ans;
    }
    private void dfs(int r,int n,int[] pos,boolean[] col,boolean[] d1,boolean[] d2,List<List<String>> ans) {
        if(r==n) {
            List<String> board=new ArrayList<>();
            for(int c:pos) { char[] row=new char[n]; Arrays.fill(row,'.'); row[c]='Q'; board.add(new String(row)); }
            ans.add(board); return;
        }
        for(int c=0;c<n;c++) {
            int a=r-c+n-1,b=r+c;
            if(col[c] || d1[a] || d2[b]) continue;
            pos[r]=c; col[c]=d1[a]=d2[b]=true;
            dfs(r+1,n,pos,col,d1,d2,ans);
            col[c]=d1[a]=d2[b]=false; // 离开当前放置，撤销所有占用标记
        }
    }
}
