import java.util.*;
class Solution {
    public int orangesRotting(int[][] grid) {
        int m=grid.length,n=grid[0].length,fresh=0,minutes=0;
        Queue<Integer> q=new ArrayDeque<>();
        for(int i=0;i<m;i++) for(int j=0;j<n;j++) {
            if(grid[i][j]==2) q.offer(i*n+j); else if(grid[i][j]==1) fresh++;
        }
        int[] dr={1,-1,0,0},dc={0,0,1,-1};
        while(fresh>0 && !q.isEmpty()) {
            int size=q.size();
            for(int i=0;i<size;i++) {
                int p=q.poll(),r=p/n,c=p%n;
                for(int d=0;d<4;d++) {
                    int x=r+dr[d],y=c+dc[d];
                    if(x>=0 && x<m && y>=0 && y<n && grid[x][y]==1) {
                        grid[x][y]=2; fresh--; q.offer(x*n+y); // 下一分钟的源
                    }
                }
            }
            minutes++;
        }
        return fresh==0?minutes:-1;
    }
}
