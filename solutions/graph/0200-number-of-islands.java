import java.util.*;
class Solution {
    public int numIslands(char[][] grid) {
        int m=grid.length,n=grid[0].length,ans=0;
        int[] dr={1,-1,0,0},dc={0,0,1,-1};
        Deque<Integer> stack=new ArrayDeque<>();
        for(int r=0;r<m;r++) for(int c=0;c<n;c++) {
            if(grid[r][c]!='1') continue;
            ans++; grid[r][c]='0'; stack.push(r*n+c);
            while(!stack.isEmpty()) {
                int p=stack.pop(),x=p/n,y=p%n;
                for(int d=0;d<4;d++) {
                    int a=x+dr[d],b=y+dc[d];
                    if(a>=0 && a<m && b>=0 && b<n && grid[a][b]=='1') {
                        grid[a][b]='0'; stack.push(a*n+b); // 入栈即标记，杜绝重复
                    }
                }
            }
        }
        return ans;
    }
}
