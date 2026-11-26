class Solution {
    public boolean exist(char[][] board,String word) {
        for(int r=0;r<board.length;r++) for(int c=0;c<board[0].length;c++) {
            if(dfs(board,word,r,c,0)) return true;
        }
        return false;
    }
    private boolean dfs(char[][] b,String s,int r,int c,int k) {
        if(r<0 || r>=b.length || c<0 || c>=b[0].length || b[r][c]!=s.charAt(k)) return false;
        if(k==s.length()-1) return true;
        char saved=b[r][c]; b[r][c]='#'; // 本路径禁止重复使用当前格
        boolean ok=dfs(b,s,r+1,c,k+1)||dfs(b,s,r-1,c,k+1)||dfs(b,s,r,c+1,k+1)||dfs(b,s,r,c-1,k+1);
        b[r][c]=saved; // 无论成功失败，都恢复供其他分支使用
        return ok;
    }
}
